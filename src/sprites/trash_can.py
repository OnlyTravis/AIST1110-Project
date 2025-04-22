from pygame.surface import Surface

from src.classes.state import GameState
from src.classes.images import ImageLoader, Images
from src.classes.game_object import GameObject

class TrashCan(GameObject):
    def __init__(self, x, y, size=60):
        super().__init__(x, y, True)
        self.size = size
        self.frames = ImageLoader.get_frames(Images.TrashCan, 32, self.size, self.size)
    
    def draw(self, screen: Surface, state: GameState):
        half = self.size / 2
        if state.player1_near == self:
            screen.blit(self.frames[1], (self.x-half, self.y-half))
        elif state.player2_near == self:
            screen.blit(self.frames[2], (self.x-half, self.y-half))
        else:
            screen.blit(self.frames[0], (self.x-half, self.y-half))

    def update(self, state, dt):
        pass