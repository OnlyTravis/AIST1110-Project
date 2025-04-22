from __future__ import annotations

from pygame import font, draw
from pygame.surface import Surface
from string import ascii_uppercase
from random import choice

from src.classes.state import GameState
from src.classes.images import ImageLoader, Images
from src.classes.game_object import GameObject

class Letter(GameObject):
    def __init__(self,
                 chr: str,
                 x: float,
                 y: float,
                 size=45,
                 interactable=3):
        super().__init__(x, y, interactable)
        self.size = size
        self.frames = ImageLoader.get_frames(Images.Letter, 32, self.size, self.size)
        self.set_char(chr)
    
    @classmethod
    def random(cls, x: float, y: float, size=45, interactable=3):
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
        chr_font = font.Font(font.get_default_font(), round(self.size*0.5))
        self.chr_text = chr_font.render(self.chr, True, "white")
    
    def set_size(self, size: int):
        """
        Sets The Size of the Letter Object
        """
        self.size = size
        self.frames = ImageLoader.get_frames(Images.Letter, 32, self.size, self.size)
        self.set_char(self.chr)
    
    def clone(self) -> "Letter":
        """
        Creates a clone of the current Letter
        """
        clone = self.__class__(self.chr, self.x, self.y, self.size, self.interactable)
        return clone

    def draw(self, screen: Surface, state: GameState):
        pos = (self.x-self.size/2, self.y-self.size/2)
        
        if state.player1_near == self:
            screen.blit(self.frames[1], pos)
        elif state.player2_near == self:
            screen.blit(self.frames[2], pos)
        else:
            screen.blit(self.frames[0], pos)
        chr_rect = self.chr_text.get_rect(center=(self.x-self.size*0.1, self.y-self.size*0.15))
        screen.blit(self.chr_text, chr_rect)
    
    def update(self, state: GameState, dt):
        # 2. todo: animation update
        pass

    def on_interact(self, player, state: GameState):
        if player.is_holding:
            # Swap Holding with the one on conveyor belt
            tmp = self.chr
            self.set_char(self.holding.chr)
            self.holding.set_char(tmp)
        else:
            # Picks up a Letter from conveyor belt
            player.holding = self.clone()
            player.holding.interactable = 0
            player.holding.set_size(40)
            player.set_holding(state, True)
            self.kill()
        return