from typing import Callable
from pygame.color import Color
from pygame.surface import Surface

from src.ui_element.button import Button
from src.ui_element.text import Text, TextAlign

class TextButton(Button):
    def __init__(self, 
                 x: float,
                 y: float,
                 w: float,
                 h: float, 
                 text: str,
                 on_click: Callable,
                 color="black",
                 font_size: int=30,
                 align: TextAlign=TextAlign.Center,
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
        self.text = Text(x, y, text, color, font_size, align)
    
    def draw(self, screen: Surface):
        super().draw(screen)
        self.text.draw(screen)
    
    def update(self, dt: float):
        super().update(dt)
        self.text.update(dt)