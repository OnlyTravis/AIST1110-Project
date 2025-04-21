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
        self.is_near_player = False  # Different display when near player
        self.set_char(chr)
    
    @classmethod
    def random(cls, x: float, y: float, size=45, interactable=True):
        """
        Creates a Letter Object with random attributes.
        (e.g. Character, Score[if we add later])
        """
        return cls(choice(ascii_uppercase), x, y, size, interactable)
    
    def set_char(self, chr: str):
        self.chr = chr
        chr_font = font.Font(font.get_default_font(), self.size-2)
        self.chr_text = chr_font.render(self.chr, True, "white")
    
    def clone(self) -> "Letter":
        clone = self.__class__(self.chr, self.x, self.y, self.size, self.interactable)
        return clone

    def draw(self, screen: Surface):
        rect = (self.x-self.size/2, self.y-self.size/2, self.size, self.size)
        
        if self.is_near_player and self.interactable:
            draw.rect(screen, "red", rect)
        else:
            draw.rect(screen, "black", rect)
        chr_rect = self.chr_text.get_rect(center=(self.x, self.y))
        screen.blit(self.chr_text, chr_rect)
    
    def update(self, state, dt):
        # 1. Check if near any player
        self.is_near_player = (self.distance_to(state.player1_pos) < INTERACT_DISTANCE)
        if not self.is_near_player and state.gamemode == Gamemode.LocalMultiplayer:
            self.is_near_player = (self.distance_to(state.player2_pos) < INTERACT_DISTANCE)
        
        # 2. todo: animation update
        pass