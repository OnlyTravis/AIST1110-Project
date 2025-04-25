from typing import Callable
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
                 background_color: Color=Color(150, 150, 150),
                 border_radius: int=0):
        Button.__init__(
            self, 
            x, 
            y, 
            w, 
            h, 
            on_click,
            background_color,
            border_radius
        )
        self.img = Image(x, y, w, h, img)
    
    def draw(self, screen: Surface):
        super().draw(screen)
        self.img.draw(screen)
    
    def update(self, dt: float):
        super().update(dt)
        self.img.update(dt)