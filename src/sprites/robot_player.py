from enum import Enum

from src.classes.event import GameEvent
from src.classes.state import GameState
from src.sprites.player import Player

class Action(Enum):
    Idle = 0
    PickingUpLetter = 1
    PlacingLetter = 2


class RobotPlayer(Player):
    def __init__(self, x, y, movable_area):
        super().__init__(x, y, False, movable_area)
        self.interact_next_frame = False
        self.action = None
        self.navigating = False
        self.navigating_to = (0, 0)
    
    def navigate_to(self, x, y):
        self.navigating = True
        self.navigating_to = (x, y)
    
    def _navigate_update(self, state: GameState, dt: float):
        if not self.navigating:
            return

        dx = self.navigating_to[0]-self.x
        dy = self.navigating_to[1]-self.y

        if 0.5 < abs(dx/dy) < 2:
            # Walk diagonally
            self.walk(state, 1 if dx > 0 else -1, 1 if dy > 0 else -1, dt)
        elif dx > dy:
            self.walk(state, 1 if dx > 0 else -1, 0, dt)
        else:
            self.walk(state, 0, 1 if dy > 0 else -1, dt)
            
        d = self.distance_to(self.navigation_pos)
        if d < 10:
            self.navigating = False

    def update(self, state: GameState, dt: float):
        # 1. Navigation
        self._navigate_update(state, dt)

        # 2. Interact
        if self.interact_next_frame:
            self.interact(state, state.player2_near)
            self.interact_next_frame = False