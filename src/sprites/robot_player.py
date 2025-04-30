from enum import Enum
from random import choice
from pygame.sprite import Group

from src.classes.state import GameState
from src.classes.event import GameEvent
from src.classes.data_classes import Question
from src.sprites.letter import Letter
from src.sprites.player import Player
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, INTERACT_DISTANCE

SUBMIT_BUTTON = (SCREEN_WIDTH/2+70, 270)
SUBMIT_AREA = (0.75*SCREEN_WIDTH-50, 250)
TRASH_CAN = (SCREEN_WIDTH/2, 270)

class Action(Enum):
    Idle = 0
    SearchingLetter = 1
    PickingUpLetter = 2
    PlacingLetter = 3
    PressSubmitButton = 4
    TrashHolding = 5

class RobotPlayer(Player):
    def __init__(self, x, y, movable_area):
        super().__init__(x, y, False, movable_area)
        self.interact_next_frame = False
        self.action = Action.Idle
        self.idle_timer = 1

        self.navigating = False
        self.navigating_to = (0, 0)
        self.navigating_threshold = 0

        self.target_letter = Group()
        self.target_chr = ""
        self.target_position = -1  # Position to put in SubmittionArea

        self.target_answer = ""
        self.submitted = ""
        self.searching: list[str] = []
        self.answer_list: list[str] = []
        self.available_answer: list[str] = []
        self.add_event_listener(GameEvent.UpdateQuestion, self._on_update_question)
        self.add_event_listener(GameEvent.SubmitStatus, self._on_answer_submit)
    
    def navigate_to(self, x, y, threshold=INTERACT_DISTANCE):
        """
        absolute = False : only get close to interactable distance
        absolute = True  : get close to 10 units away
        """
        self.navigating = True
        self.navigating_threshold = threshold
        self.navigating_to = (x, y)
    
    def _navigate_update(self, state: GameState, dt: float):
        """
        Update function for when the robot is navigating
        to a certain point
        """
        if not self.navigating:
            return

        dx = self.navigating_to[0]-self.x
        dy = self.navigating_to[1]-self.y

        if abs(self.x - self.movable_area[0]) < 2 and dx < 0:
            dx = 0
        if abs(self.x - self.movable_area[2]) < 2 and dx > 0:
            dx = 0
        if abs(self.y - self.movable_area[1]) < 2 and dy < 0:
            dy = 0
        if abs(self.y - self.movable_area[3]) < 2 and dy > 0:
            dy = 0

        if dx == 0:
            dx = 0.01
        if dy == 0:
            dy = 0.01

        if 0.5 < abs(dx/dy) < 2:
            # Walk diagonally
            self.walk(state, 1 if dx > 0 else -1, 1 if dy > 0 else -1, dt)
        elif abs(dx) > abs(dy):
            self.walk(state, 1 if dx > 0 else -1, 0, dt)
        else:
            self.walk(state, 0, 1 if dy > 0 else -1, dt)
            
        d = self.distance_to(self.navigating_to)
        if d < self.navigating_threshold:
            self.navigating = False

    def update(self, state: GameState, dt: float):
        # 1. Choose a target answer if none is selected
        if self.target_answer == "" and len(self.available_answer) != 0:
            self.target_answer = choice(self.available_answer)
        
        # 2. Check Submitted letters
        for letter in self.submitted:
            if letter not in self.target_answer:
                self.action = Action.PressSubmitButton
                self.navigate_to(*SUBMIT_BUTTON, threshold=25)
                break

        # 3. Navigation
        self._navigate_update(state, dt)

        # 4. Check Action
        match self.action:
            case Action.Idle:
                self.idle_timer -= dt
                if self.idle_timer < 0:
                    self.next_action()

            case Action.PickingUpLetter:
                # Check if letter is gone / been picked up
                letters = self.target_letter.sprites()
                if len(letters) == 0 or letters[0].chr != self.target_chr:
                    self.action = Action.Idle
                    self.idle_timer = 1
                    return

                # Pick up letter if near
                if self.navigating == False and state.player2_near != None:
                    self.target_letter.empty()
                    self.interact(state, state.player2_near)
                    self.action = Action.Idle
                    self.idle_timer = 1
                    return
            
                # Navigate to new position of letter
                letter = letters[0]
                self.navigate_to(letter.x, letter.y, threshold=45)

            case Action.PlacingLetter:
                if self.navigating == False and state.player2_near != None:
                    pos = self.target_position
                    length = len(self.submitted)
                    self.submitted = self.submitted[0:pos] + self.holding.chr.lower() + self.submitted[pos: length]
                    self.interact(state, state.player2_near)
                    self.action = Action.Idle

            case Action.PressSubmitButton:
                if self.navigating == False and state.player2_near != None:
                    self.interact(state, state.player2_near)
                    self.submitted = ""
                    self.action = Action.Idle
                    self.idle_timer = 2
            
            case Action.TrashHolding:
                if self.navigating == False and state.player2_near != None:
                    self.interact(state, state.player2_near)
                    self.action = Action.Idle
                    self.idle_timer = 1

            case Action.SearchingLetter:
                letters: list[Letter] = state.letters.sprites()
                for i in range(len(letters)-1, -1, -1):
                    letter = letters[i]
                    if letter.chr.lower() in self.searching:
                        self.action = Action.PickingUpLetter
                        self.searching = []
                        self.target_letter.add(letter)
                        self.target_chr = letter.chr
                        self.navigate_to(letter.x, letter.y, threshold=45)

    def next_action(self):
        """
        Update self.action based on current situation
        """
        # 1. Check for SubmitAnswer
        if self.submitted == self.target_answer.lower():
            self.action = Action.PressSubmitButton
            self.navigate_to(*SUBMIT_BUTTON, threshold=25)
            return

        # 1. Check for PlacingLetter & TrashHolding
        if self.is_holding:
            holding = self.holding.chr.lower()
            length = len(self.submitted)
            l, r = 0, 0
            ghost_pos = 0
            while r < len(self.target_answer):
                if l < length and self.submitted[l] == self.target_answer[r]:
                    l += 1
                    r += 1
                elif self.target_answer[r] == holding:
                    ghost_pos = l
                    break
                else:
                    r += 1

            if r == len(self.target_answer):
                self.action = Action.TrashHolding
                self.navigate_to(*TRASH_CAN, threshold=25)
            else:
                self.action = Action.PlacingLetter
                x = SUBMIT_AREA[0] - length*40/2 + ghost_pos*40
                y = 290
                self.target_position = ghost_pos
                self.navigate_to(x, y, threshold=10)
            return

        # 2. Check if letter missing from submitted
        missing = []
        length = len(self.submitted)
        l, r = 0, 0
        for letter in self.target_answer:
            if l < length and self.submitted[l] == self.target_answer[r]:
                l += 1
            else:
                missing.append(self.target_answer[r].lower())
            r += 1

        if length != 0 and l != length:  # Letters in submitted does not match with target answer
            self.action = Action.PressSubmitButton
            self.navigate_to(*SUBMIT_BUTTON, threshold=25)
            return
        
        # 3. Find missing letter 
        if len(missing) > 0:
            self.action = Action.SearchingLetter
            self.searching = missing
            return

    def _on_answer_submit(self, event):
        """
        Check if the opponent submitting the target answer.
        Remove submitted answer from answer pool
        """
        if not event.is_correct:
            return
        
        answer = self.answer_list[event.answer_index]
        self.available_answer.remove(answer)
        if self.target_answer == answer:
            self.target_answer = choice(self.available_answer)
    
    def _on_update_question(self, event):
        question: Question = event.question
        self.answer_list = [answer.text.lower() for answer in question.answers]
        self.available_answer = [answer.text.lower() for answer in question.answers]
        self.target_answer = ""