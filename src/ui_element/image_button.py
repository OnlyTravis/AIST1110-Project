from typing import Callable
from pygame import BLEND_RGB_ADD
from pygame.color import Color
from pygame.surface import Surface

from src.classes.images import Images
from src.ui_element.button import Button
from src.ui_element.image import Image

class ImageButton(Button):
    def __init__(self, 
                 x: float,
                 y: float,
                 w: float,
                 h: float, 
                 img: Images,
                 on_click: Callable,
                 background_color: Color=None,
                 border_radius: int=0):
        super().__init__(
            x, 
            y, 
            w, 
            h, 
            on_click,
            background_color,
            border_radius
        )
        self.img = Image(x, y, w, h, img)
        self.img_hover = Image(x, y, w, h, img)
        self.img_hover.img.fill((10, 10, 10), special_flags=BLEND_RGB_ADD)
    
    def draw(self, screen: Surface):
        super().draw(screen)
        if self.is_hover:
            self.img_hover.draw(screen)
        else:
            self.img.draw(screen)
    
    def update(self, dt: float):
        super().update(dt)
        self.img.update(dt)
    
    def kill(self):
        super().kill()
        self.img.kill()