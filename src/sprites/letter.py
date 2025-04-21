from pygame import font, draw
from pygame.surface import Surface
from string import ascii_uppercase
from random import choice

from src.classes.state import Gamemode
from src.classes.game_object import GameObject
from src.constants import INTERACT_DISTANCE

class Letter(GameObject):
    def __init__(self,
                 chr: str,
                 x: float,
                 y: float,
                 size=45,
                 interactable=True):
        super().__init__(x, y, interactable)
        self.size = size
        self.set_char(chr)
    
    @classmethod
    def random(cls, x: float, y: float, size=45, interactable=True):
        """
        Creates a Letter Object with random attributes.
        (e.g. Character, Score[if we add later])
        """
        return cls(choice(ascii_uppercase), x, y, size, interactable)
    
    def set_char(self, chr: str):
        """
        Sets Displayed Letter to 'chr'.
        """
        self.chr = chr
        chr_font = font.Font(font.get_default_font(), self.size-2)
        self.chr_text = chr_font.render(self.chr, True, "white")
    
    def clone(self) -> "Letter":
        """
        Creates a clone of the current Letter
        """
        clone = self.__class__(self.chr, self.x, self.y, self.size, self.interactable)
        return clone

    def draw(self, screen: Surface):
        rect = (self.x-self.size/2, self.y-self.size/2, self.size, self.size)
        
        if self.near_player != 0:
            draw.rect(screen, "red", rect)
        else:
            draw.rect(screen, "black", rect)
        chr_rect = self.chr_text.get_rect(center=(self.x, self.y))
        screen.blit(self.chr_text, chr_rect)
    
    def update(self, state, dt):
        super().update(state, dt)
        
        # 2. todo: animation update
        pass