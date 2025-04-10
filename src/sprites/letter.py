from pygame import font, draw
from pygame.surface import Surface
from math import dist

from src.classes.game_object import GameObject
from src.constants import DETECT_DISTANCE

class Letter(GameObject):
    def __init__(self,
                 chr: str,
                 x: float,
                 y: float,
                 size=45,
                 disabled=False):
        super().__init__()
        self.chr = chr
        self.size = size
        self.x = x
        self.y = y
        self.is_near_player = False  # Different display when near player
        self.disabled = disabled  # For displaying in hand
        self.init_display()
    
    def init_display(self):
        chr_font = font.Font(font.get_default_font(), self.size-2)
        self.chr_text = chr_font.render(self.chr, True, "white")
        self.chr_rect = self.chr_text.get_rect(center=(self.x, self.y))

    def draw(self, screen: Surface):
        rect = (self.x-self.size/2, self.y-self.size/2, self.size, self.size)
        
        if self.is_near_player and not self.disabled:
            draw.rect(screen, "red", rect)
        else:
            draw.rect(screen, "black", rect)
        screen.blit(self.chr_text, self.chr_rect)
    
    def check_is_near(self, player_x, player_y):
        d = dist((self.x, self.y), (player_x, player_y))
        self.is_near_player = (d >= DETECT_DISTANCE)
