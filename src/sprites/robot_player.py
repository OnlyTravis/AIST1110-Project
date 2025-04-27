from pygame import key
from pygame.event import Event

from src.classes.state import GameState
from src.sprites.player import Player

class RobotPlayer(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.interact_next_frame = False
        self.navigating = False
        self.navigation_pos = (0, 0)
    
    def _navigate_to(self, x, y):
        self.navigating = True
        self.navigation_pos = (x, y)

    def update(self, state: GameState, dt: float):
        # 1. Navigation
        if self.navigating:
            pass

        # 2. Interact
        if self.interact_next_frame:
            self.interact(state, state.player2_near)
            self.interact_next_frame = False