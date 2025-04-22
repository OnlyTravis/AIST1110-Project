from pygame.surface import Surface

from src.classes.state import GameState
from src.classes.game_object import GameObject
from src.sprites.player import Player

"""
    Player holding Letter
    -> SubmitArea interactable, Letters not interactable
    (Can place letter on the area)
    
    Player not holding Letter
    -> SubmitArea not interactable, Letters interactable
    (Can remove letter from the area)
"""

class SubmitArea(GameObject):
    def __init__(self, 
                 x, 
                 y, 
                 is_p1=True):
        super().__init__(x, y, 1 if is_p1 else 2, True)
        self.is_p1 = is_p1
    
    def update(self, state: GameState, dt: float):
        self._update_interactability(state)

        if ((self.is_p1 and state.player1_near == self) or
            (not self.is_p1 and state.player2_near == self)):
            pass # change display
    
    def on_interact(self, player: Player, state: GameState):
        pass

    def _update_interactability(self, state: GameState):
        inner_objects: list[GameObject] = self.inner_objects.sprites()
        interactable = self.interactable = 1 if self.is_p1 else 2

        if (self.is_p1 and state.player1_is_holding) or (not self.is_p1 and state.player2_is_holding):
            self.interactable = interactable
            for obj in inner_objects:
                obj.interactable = 0
        else: 
            self.interactable = 0
            for obj in inner_objects:
                obj.interactable = self.interactable = interactable