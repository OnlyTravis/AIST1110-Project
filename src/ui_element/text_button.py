from typing import Callable
from pygame.color import Color
from pygame.surface import Surface

from src.ui_element.button import Button
from src.ui_element.text import Text, TextAlign

class TextButton(Button):
    def __init__(self, 
                 text: str,
                 x: float,
                 y: float,
                 on_click: Callable,
                 w: float=-1,
                 h: float=-1,
                 color="black",
                 font_size: int=30,
                 align: TextAlign=TextAlign.Center,
                 background_color: Color=Color(150, 150, 150),
                 border_radius: int=0):
        """
        w / h = -1 : Auto adjust size based on text
        """
        self.text = Text(x, y, text, color, font_size, align)
        w = self.text.text_rect.w+20
        h = self.text.text_rect.h+20
        
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
    
    def draw(self, screen: Surface):
        super().draw(screen)
        self.text.draw(screen)
    
    def update(self, dt: float):
        super().update(dt)
        self.text.update(dt)