from collections.abc import Callable
from random import randint
from pygame import KEYDOWN, event, surface

from src.classes.scene import Scene
from src.classes.event import event_handler
from src.classes.images import Images
from src.classes.scene import Scenes
from src.ui_element.image import Image
from src.ui_element.letter import LetterDisplay
from src.ui_element.text import Text

class TitleScreen(Scene):
    def __init__(self, screen: surface.Surface, to_scene: Callable):
        super().__init__(screen, to_scene)

        listener_id = event_handler.add_listener(KEYDOWN, self.on_key_down)
        self.listeners.append(listener_id)

        # Init texts
        self._set_up_ui()

    def _set_up_ui(self):
        w, h = self.screen.get_size()
        # 1. Add Background
        self.add_element(Image(w/2, h/2, w, h, Images.Background1))

        # 2. Title Text
        title_text = "Guess The Answer"
        x = w/2 - 60*len(title_text)/2
        y = 150
        for chr in title_text:
            if chr != " ":
                self.add_element(LetterDisplay(chr, x, y+randint(-5, 5), 55))
            x += 60
        self.add_element(Text(w/2, h/2+100, "Press Any Key To Start", color=(100, 100, 100), font_size=50))

    def draw(self):
        super().draw()
    
    def update(self, dt):
        super().update(dt)

    def on_key_down(self, event: event.Event):
        self.exit_to(Scenes.OptionScreen)