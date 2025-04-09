from collections.abc import Callable
from pygame import surface

from src.games.scene import Scene
from src.games.event import event_handler

class GameScene(Scene):
    def __init__(self, screen: surface.Surface, toScene: Callable):
        super().__init__(screen, toScene)

    def draw(self):
        w, h = self.screen.get_size()

        # Draw texts
        self.screen.fill("white")
    
    def update(self):
        pass