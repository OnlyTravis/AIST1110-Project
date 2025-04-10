from pygame import key, K_w, K_a, K_s, K_d, K_UP, K_DOWN, K_LEFT, K_RIGHT

from src.classes.state import GameState
from src.sprites.player import Player

class HumanPlayer(Player):
    def __init__(self, x, y, is_p1):
        super().__init__(x, y, is_p1)
        if is_p1:
            self.key_set = [K_w, K_s, K_a, K_d]
        else:
            self.key_set = [K_UP, K_DOWN, K_LEFT, K_RIGHT]  # Local Multiplayer
    
    def update(self, state: GameState, dt: float):
        super().update(state, dt)
        
        # 1. Checks Key Presses
        keys = key.get_pressed()
        dir = [0, 0]
        if keys[self.key_set[0]]:
            dir[1] -= 1
        if keys[self.key_set[1]]:
            dir[1] += 1
        if keys[self.key_set[2]]:
            dir[0] -= 1
        if keys[self.key_set[3]]:
            dir[0] += 1
        self.walk(state, dir[0], dir[1], dt)