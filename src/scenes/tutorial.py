from pygame import surface

from src.games.scene import Scene

class TutorialScreen(Scene):
    def __init__(self, screen: surface.Surface, toScene):
        super().__init__(toScene)

        self.screen = screen

    def draw(self):
        self.screen.fill("red")