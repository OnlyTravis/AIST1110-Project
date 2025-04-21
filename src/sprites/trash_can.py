from pygame.surface import Surface
from src.classes.game_object import GameObject

class TrashCan(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, True)
    
    def draw(self, screen: Surface):
        pass

    def update(self, state, dt):
        super().update(state, dt)