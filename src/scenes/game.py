from collections.abc import Callable
from pygame import KEYDOWN
from pygame.surface import Surface
from pygame.sprite import Group
from pygame.event import Event

from src.classes.game_manager import GameManager, GameEvent
from src.classes.game_object import GameObject
from src.classes.state import States, GameState, Gamemode
from src.classes.scene import Scene
from src.classes.images import Images
from src.sprites.human_player import HumanPlayer
from src.sprites.conveyor import ConveyorBelt
from src.sprites.trash_can import TrashCan
from src.sprites.submit_area import SubmitArea
from src.sprites.submit_button import SubmitButton
from src.sprites.timer import Timer
from src.ui_element.question_box import QuestionBox
from src.ui_element.result_display import ResultDisplay
from src.ui_element.score_display import ScoreDisplay
from src.ui_element.image_button import ImageButton
from src.constants import INTERACT_DISTANCE

class GameScreen(Scene):
    def __init__(self, screen: Surface, toScene: Callable):
        super().__init__(screen, toScene)

        self.state = GameState()
        self.manager = GameManager(self.state)
        self._init_ui()
        self._init_objects()
        self._init_game_state()
        self.add_event_listener(KEYDOWN, self._handle_key_down)
        self.add_event_listener(GameEvent.GameStart, self._on_game_start)
        self.add_event_listener(GameEvent.SubmitStatus, self._on_submit)

    def _init_ui(self):
        w, h = self.screen.get_size()
        self.add_element(QuestionBox(w/2, 110))
        self.add_element(ImageButton(w-50, 50, 70, 70, Images.PauseButton, self._on_pause))
        self.add_element(ScoreDisplay(100, 50, True))
        self.add_element(ScoreDisplay(w-100, 50, False))

    def _init_objects(self):
        w, h = self.screen.get_size()
        self.objs = Group()
        self.objs.add(ConveyorBelt(w/2-400, 280, 300, False))
        self.objs.add(ConveyorBelt(w/2+400, 280, 300, False))
        self.objs.add(ConveyorBelt(w/2-375, 605, 340, True))
        self.objs.add(ConveyorBelt(w/2+40, 605, 340, True, False))
        self.objs.add(ConveyorBelt(w/2-25, 280, 300, False))
        self.objs.add(ConveyorBelt(w/2+25, 280, 300, False))
        self.objs.add(TrashCan(w/2-175, 430))
        self.objs.add(TrashCan(w/2+175, 430))
        self.objs.add(SubmitArea(w/2-200, 250, 200, True))
        self.objs.add(SubmitArea(w/2+200, 250, 200, False))
        self.objs.add(SubmitButton(w/2-50, 250))
        self.objs.add(SubmitButton(w/2+50, 250, False))
        self.objs.add(Timer(w-100, 110))

        self.player1 = HumanPlayer(w/2-100, h/2, True)
        self.player2 = HumanPlayer(w/2+100, h/2, False)

    def _init_game_state(self):
        self.state.player1_pos = (self.player1.x, self.player1.y)
        self.state.gamemode = Gamemode.LocalMultiplayer # Add change gamemode later

    def draw(self):
        self.screen.fill(color=(200,200,200))
        
        for obj in self.objs.sprites():
            obj.draw(self.screen, self.state)
        self.player1.draw(self.screen, self.state)
        self.player2.draw(self.screen, self.state)

        super().draw()

    def update(self, dt):
        if self.state.game_state == States.Playing:
            self._check_player_near(self.objs.sprites())

            for obj in self.objs.sprites():
                obj.update(self.state, dt)
            self.player1.update(self.state, dt)
            self.player2.update(self.state, dt)

            self.manager.update(self.state, dt)

        super().update(dt)
    
    def _handle_key_down(self, event: Event):
        """
        Handles KEYDOWN events (e.g. menu_open...)
        """
        pass

    def _on_game_start(self, event: Event):
        """
        Change GameState, Display first question
        """
        self.state.game_state = States.Playing

    def _on_submit(self, event: Event):
        # Add Correct/Incorrect Display
        w, h = self.screen.get_size()
        x = w/3 if event.is_p1 else 2*w/3
        self.add_element(ResultDisplay(x, 430, event.is_correct))
    
    def _on_pause(self):
        GameEvent.GamePause.post()

    def _check_player_near(self, objs):
        """
        Updates player1_near & player2_near state
        """
        self.state.player1_near = None
        self.state.player2_near = None

        def check_group(objs: list[GameObject]) -> list[tuple[float, GameObject]]:
            closest1 = (1e10, None)
            closest2 = (1e10, None)
            for obj in objs:
                if obj.recursive:
                    closest = check_group(obj.inner_objects.sprites())
                    if closest[0][0] < closest1[0]:
                        closest1 = closest[0]
                    if closest[1][0] < closest2[0]:
                        closest2 = closest[1]

                if obj.can_interact_with_p1:
                    d1 = obj.distance_to(self.state.player1_pos)
                    if d1 < closest1[0]:
                        closest1 = (d1, obj)

                if self.state.gamemode != Gamemode.LocalMultiplayer:
                    continue

                if obj.can_interact_with_p2:
                    d2 = obj.distance_to(self.state.player2_pos)
                    if d2 < closest2[0]:
                        closest2 = (d2, obj)
            return [closest1, closest2]
        
        closest1, closest2 = check_group(objs)
        if closest1[0] < INTERACT_DISTANCE:
            self.state.player1_near = closest1[1]
        if closest2[0] < INTERACT_DISTANCE:
            self.state.player2_near = closest2[1]
