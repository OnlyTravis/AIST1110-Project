from collections.abc import Callable
from pygame import KEYDOWN, K_SPACE, event, surface, font

from src.games.scene import Scene
from src.games.event import event_handler
from src.scenes.tutorial import TutorialScreen

class TitleScreen(Scene):
    def __init__(self, screen: surface.Surface, toScene: Callable):
        super().__init__(toScene)

        self.screen = screen

        listener_id = event_handler.addListener(KEYDOWN, self.onKeyDown)
        self.listeners.append(listener_id)

        # temperary
        font_1 = font.Font(font.get_default_font(), 40)
        self.text = font_1.render("Title Screen", True, "black")

    def draw(self):
        self.screen.fill("gray")
        self.screen.blit(self.text, (self.screen.get_width()/2, self.screen.get_height()/2))

    def onKeyDown(self, event: event.Event):
        print(event)
        if event.key == K_SPACE:
            self.exitTo(TutorialScreen)