from pygame.surface import Surface

from src.classes.game_object import GameObject
from src.classes.images import ImageLoader, Images
from src.classes.state import GameState
from src.classes.event import GameEvent
from src.sprites.player import Player

class SubmitButton(GameObject):
    def __init__(self, x, y, is_p1=True):
        super().__init__(x, y, 1 if is_p1 else 2)

        self.is_p1 = is_p1
        self.size = 60
        self.frames = ImageLoader.get_frames(Images.SubmitButton, 32, self.size, self.size)
    
    def draw(self, screen: Surface, state: GameState):
        corner = self.get_pos((-self.size/2, -self.size/2))
        if state.player1_near == self:
            screen.blit(self.frames[1], corner)
        elif state.player2_near == self:
            screen.blit(self.frames[2], corner)
        else:
            screen.blit(self.frames[0], corner)
    
    def on_interact(self, player: Player, state: GameState):
        GameEvent.post(GameEvent.SubmitButtonPressed, {"is_p1": self.is_p1})