from math import dist
from pygame import draw, transform
from pygame.sprite import Group
from pygame.surface import Surface

from src.classes.images import ImageLoader, Images
from src.classes.state import GameState
from src.classes.game_object import GameObject
from src.classes.event import GameEvent
from src.sprites.player import Player
from src.sprites.letter import Letter

LETTER_SIZE = 35
LETTER_SEPARATION = 40

class SubmitArea(GameObject):
    def __init__(self,
                 x,
                 y,
                 width=200,
                 is_p1=True):
        super().__init__(x, y, 1 if is_p1 else 2, True)
        self.width = width
        self.is_p1 = is_p1
        self.ghost_pos = -1
        self.is_near_player = False  # To detect when player_near is changed and update displays
        self.letter_count = 0

        frame_indice = [0, 1, 2] if is_p1 else [3, 4, 5]
        self.frames = ImageLoader.get_frames(Images.SubmitTable, 32, 80, 80, frame_indice)
        self.frames[1] = transform.scale(self.frames[1], (self.width-160, 80))

        self.falling = Group()        
        self.add_event_listener(GameEvent.SubmitButtonPressed, self._on_submit)
    
    def draw(self, screen: Surface, state: GameState):
        # 1. Draw Table
        half = self.width / 2
        screen.blit(self.frames[0], (self.x - half, self.y - 40))
        screen.blit(self.frames[1], (self.x - half + 80, self.y - 40))
        screen.blit(self.frames[2], (self.x + half - 80, self.y - 40))

        # 2. Draw Letters on table
        for obj in self.inner_objects.sprites():
            obj.draw(screen, state)
        for obj in self.falling.sprites():
            obj.draw(screen, state)
        
        # 3. Draw ghost if player is near and holding letter
        if self.ghost_pos != -1:
            n = len(self.inner_objects.sprites())
            x = self.x - n*LETTER_SEPARATION/2 + self.ghost_pos*LETTER_SEPARATION
            offset = LETTER_SIZE/2
            if self.is_p1:
                draw.rect(screen, "red", (x-offset, self.y-offset-5, 2*offset, 2*offset), border_radius=10)
            else:
                draw.rect(screen, "blue", (x-offset, self.y-offset-5, 2*offset, 2*offset), border_radius=10)

    def update(self, state: GameState, dt: float):
        # 1. Update self.interactable
        self._update_interactability(state)

        # 2. Update Letter position if needed
        can_interact = (self.interactable != 0)
        is_near_player = ((self.is_p1 and state.player1_near == self) or (not self.is_p1 and state.player2_near == self))
        if can_interact:
            if is_near_player:
                # Player can place letter
                # => Check Ghost Position & Update if needed
                player_pos = state.player1_pos if self.is_p1 else state.player2_pos
                ghost_pos = self._get_ghost_pos(player_pos)
                if self.ghost_pos != ghost_pos:
                    self.ghost_pos = ghost_pos
                    self.is_near_player = is_near_player
                    self._update_letter_positions(state)
            elif self.is_near_player:
                # Player that can place letter and just got away from the area
                # => Update Display
                self.is_near_player = is_near_player
                self.ghost_pos = -1
                self._update_letter_positions(state)
        self.is_near_player = is_near_player

        # 3. Update Letters
        super().update(state, dt)
        self.falling.update(state=state, dt=dt)
            
    
    def on_interact(self, player: Player, state: GameState):
        # Player places letter on area
        # Position according to ghost_pos
        if not player.is_holding:
            return
        
        letter = player.holding.clone()
        letter.index = self.ghost_pos
        for obj in self.inner_objects.sprites():
            if obj.index >= self.ghost_pos:
                obj.index += 1
        letter.set_size(LETTER_SIZE)
        self.inner_objects.add(letter)
        self.letter_count += 1
        self.ghost_pos = -1

        player.set_holding(state, False)
        self.interactable = 0
        self._update_letter_positions(state)

    def distance_to(self, pos) -> float:
        """
        Overwrite distance_to as the area is a large object
        """
        half = self.width / 2
        x1 = max(min(pos[0], self.x+half), self.x-half)
        return dist((x1, self.y), pos)

    
    def get_word(self) -> str:
        letters: list[Letter] = self.inner_objects.sprites()
        text_arr = [""] * len(letters)
        for obj in letters:
            text_arr[obj.index] = obj.chr
        return "".join(text_arr)

    def _on_submit(self, event):
        if event.is_p1 != self.is_p1:
            return
        
        GameEvent.post(GameEvent.SubmitWord, {
            "is_p1": self.is_p1,
            "word": self.get_word()
        })

        for letter in self.inner_objects:
            self.falling.add(letter)
            self.inner_objects.remove(letter)
            letter.fall()

    def _get_ghost_pos(self, player_pos: tuple) -> int:
        """
        Gets Letter Ghosts position (For placing letters onto the area)
        based on the player position.
        """
        n = len(self.inner_objects.sprites())
        boundary = self.x - (n-1)*LETTER_SEPARATION/2

        i = 0
        while i < n:
            if player_pos[0] < boundary:
                return i
            boundary += LETTER_SEPARATION
            i += 1
        return i

    def _update_interactability(self, state: GameState):
        """
        Update self.interactable based on if player is holding a Letter.
        Holding Letter: interactable by designated player
        Not Holding Letter: not interactable
        """
        inner_objects: list[GameObject] = self.inner_objects.sprites()
        interactable = 1 if self.is_p1 else 2

        if (self.is_p1 and state.player1_is_holding) or (not self.is_p1 and state.player2_is_holding):
            self.interactable = interactable
            for obj in inner_objects:
                obj.interactable = 0
        else: 
            self.interactable = 0
            for obj in inner_objects:
                obj.interactable = interactable
    
    def _update_letter_positions(self, state: GameState):
        """
        Updates position of letters in self.inner_object according to
        if player can place letters on the area
        """
        # 1. Check if any Letter is picked up. If yes, reorder indexes
        letters: list[Letter] = self.inner_objects.sprites()
        if len(letters) != self.letter_count:
            self.letter_count = len(letters)
            found = [False]*(len(letters)+1)
            for letter in letters:
                found[letter.index] = True
            n = found.index(False)
            for letter in letters:
                if letter.index > n:
                    letter.index -= 1

        # 2. Update Letter Positions
        if self.is_near_player and self.interactable:
            # Reserve Gap for Ghost Letter
            start_x = self.x - LETTER_SEPARATION/2*len(letters)
            for letter in letters:
                x = start_x + letter.index*LETTER_SEPARATION
                if letter.index >= self.ghost_pos:
                    x += LETTER_SEPARATION
                letter.move_to(x, self.y-5)
        else:
            # Ordinary Display
            start_x = self.x - LETTER_SEPARATION/2*(len(letters)-1)
            for letter in letters:
                letter.move_to(start_x + LETTER_SEPARATION*letter.index, self.y-5)