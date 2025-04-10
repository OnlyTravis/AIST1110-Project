from pygame import key, K_w, K_a, K_s, K_d

from src.sprites.player import Player

class HumanPlayer(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
    
    def update(self, dt):
        super().update(dt)
        
        keys = key.get_pressed()
        dir = [0, 0]
        if keys[K_w]:
            dir[1] -= 1
        if keys[K_s]:
            dir[1] += 1
        if keys[K_a]:
            dir[0] -= 1
        if keys[K_d]:
            dir[0] += 1
        self.walk(dir[0], dir[1], dt)