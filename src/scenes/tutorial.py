from collections.abc import Callable
from pygame import KEYDOWN, K_SPACE, event, surface, font

from src.classes.scene import Scene
from src.classes.event import event_handler
from src.classes.scene import Scenes

class TutorialScreen(Scene):
    def __init__(self, screen: surface.Surface, to_scene: Callable, **args):
        super().__init__(screen, to_scene)
        self.other_args = args  # Passes to GameScreen

        listener_id = event_handler.add_listener(KEYDOWN, self.on_key_down)
        self.listeners.append(listener_id)

        # Init texts
        font_1 = font.Font(font.get_default_font(), 40)
        self.title = font_1.render("Tutorial (WIP)", True, "black")
        self.tip =  font_1.render("Press Space to Start Game", True, "black")

    def draw(self):
        w, h = self.screen.get_size()

        # Draw texts
        self.screen.fill("gray")
        title_rect = self.title.get_rect(center=(w/2, h/2))
        self.screen.blit(self.title, title_rect)
        tip_rect = self.tip.get_rect(center=(w/2, h/2+130))
        self.screen.blit(self.tip, tip_rect)

    def on_key_down(self, event: event.Event):
        if event.key == K_SPACE:
            self.exit_to(Scenes.GameScreen, **self.other_args)