from __future__ import annotations

from pygame import font
from pygame.surface import Surface

from src.classes.images import ImageLoader, Images
from src.classes.ui_element import UIElement

class LetterDisplay(UIElement):
    def __init__(self,
                 chr: str,
                 x: float,
                 y: float,
                 size=45):
        super().__init__(x, y)
        self.size = size
        self.img = ImageLoader.get_frames(Images.Letter, 32, self.size, self.size)[0]
        self.chr = ""
        self.set_char(chr)
    
    def set_char(self, chr: str):
        """
        Sets Displayed Letter to chr.
        """
        if self.chr == chr:
            return

        self.chr = chr
        chr_font = font.Font(font.get_default_font(), round(self.size*0.5))
        self.chr_text = chr_font.render(self.chr, True, "white")
    
    def set_size(self, size: int):
        """
        Sets The Size of the Letter Object
        """
        self.size = size
        self.img = ImageLoader.get_frames(Images.Letter, 32, self.size, self.size)[0]
        chr_font = font.Font(font.get_default_font(), round(self.size*0.5))
        self.chr_text = chr_font.render(self.chr, True, "white")

    def draw(self, screen: Surface):
        pos = (self.x-self.size/2, self.y-self.size/2)
        screen.blit(self.img, pos)

        chr_rect = self.chr_text.get_rect(center=(self.x-self.size*0.1, self.y-self.size*0.15))
        screen.blit(self.chr_text, chr_rect)
    
    def update(self, dt):
        # 2. todo: animation update
        pass