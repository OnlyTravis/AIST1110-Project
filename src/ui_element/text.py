from enum import Enum
from pygame import font

from src.classes.ui_element import UIElement

class TextAlign(Enum):
    Start = 0
    Center = 1

class Text(UIElement):
    def __init__(self, 
                 x: float,
                 y: float,
                 text: str="",
                 color="black",
                 font_size: int=30,
                 align=TextAlign.Center):
        super().__init__(x, y)
        self.text = text
        self.color = color
        self.font_size = font_size
        self.align = align
        self._render_text()
    
    def draw(self, screen):
        screen.blit(self.rendered_text, self.text_rect)
        match self.align:
            case TextAlign.Start:
                pass
            case TextAlign.Center:
                text_rect = self.rendered_text.get_rect(center=self.pos)
                screen.blit(self.rendered_text, text_rect)

    def set_font_size(self, font_size):
        self.font_size = font_size
        self._render_text()

    def set_text(self, text):
        self.text = text
        self._render_text()
    
    def set_color(self, color):
        self.color = color
        self._render_text()

    def _render_text(self):
        text_font = font.Font(font.get_default_font(), self.font_size)
        self.rendered_text = text_font.render(self.text, True, self.color)
        match self.align:
            case TextAlign.Start:
                self.text_rect = self.rendered_text.get_rect(center=self.pos)
                self.text_rect.midleft = (self.x, self.y)
            case TextAlign.Center:
                self.text_rect = self.rendered_text.get_rect(center=self.pos)
                