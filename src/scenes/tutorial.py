from collections.abc import Callable
from pygame import KEYDOWN, K_SPACE, event, surface, font

from src.games.scene import Scene
from src.games.event import event_handler
from src.scenes.game import GameScene

class TutorialScreen(Scene):
    def __init__(self, screen: surface.Surface, toScene: Callable):
        super().__init__(toScene)

        self.screen = screen

        listener_id = event_handler.addListener(KEYDOWN, self.onKeyDown)
        self.listeners.append(listener_id)

        # Init texts
        font_1 = font.Font(font.get_default_font(), 40)
        self.title = font_1.render("Tutorial", True, "black")
        self.tip =  font_1.render("Press Space to Start Game", True, "black")

    def draw(self):
        w, h = self.screen.get_size()

        # Draw texts
        self.screen.fill("gray")
        title_rect = self.title.get_rect(center=(w/2, h/2))
        self.screen.blit(self.title, title_rect)
        tip_rect = self.tip.get_rect(center=(w/2, h/2+130))
        self.screen.blit(self.tip, tip_rect)

    def onKeyDown(self, event: event.Event):
        print(event)
        if event.key == K_SPACE:
            self.exitTo(GameScene)