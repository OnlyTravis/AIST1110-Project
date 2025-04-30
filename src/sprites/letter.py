from pygame import font
from pygame.surface import Surface
from string import ascii_uppercase
from random import choice, uniform

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
        self.chr = ""
        self.set_char(chr)

        self.is_falling = False
        self.vx = 0
        self.vy = 0
    
    @classmethod
    def random(cls, x: float, y: float, answers: list[str] = [], size=45, interactable=3):
        """
        Creates a Letter Object with random character.
        Will only choose from answers if an non-empty list is provided
        """
        if len(answers) == 0:
            return cls(choice(ascii_uppercase), x, y, size, interactable)
        else:
            return cls(choice("".join(answers)), x, y, size, interactable)
    
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
        self.frames = ImageLoader.get_frames(Images.Letter, 32, self.size, self.size)
        chr_font = font.Font(font.get_default_font(), round(self.size*0.5))
        self.chr_text = chr_font.render(self.chr, True, "white")
    
    def clone(self) -> "Letter":
        """
        Creates a clone of the current Letter
        """
        clone = self.__class__(self.chr, self.x, self.y, self.size, self.interactable)
        return clone

    def draw(self, screen: Surface, state: GameState):
        pos = (self.x-self.size/2, self.y-self.size/2)

        if self.is_falling and self.y > screen.get_height():
            self.kill()
            return
        
        if state.player1_near == self:
            screen.blit(self.frames[1], pos)
        elif state.player2_near == self:
            screen.blit(self.frames[2], pos)
        else:
            screen.blit(self.frames[0], pos)

        chr_rect = self.chr_text.get_rect(center=(self.x-self.size*0.1, self.y-self.size*0.15))
        screen.blit(self.chr_text, chr_rect)
    
    def update(self, state: GameState, dt: float):
        if self.is_falling:
            self.x += self.vx*dt
            self.y += self.vy*dt
            self.vy += 1000*dt

    def on_interact(self, player, state: GameState):
        if player.is_holding:
            # Swap Holding with the one on conveyor belt
            tmp = self.chr
            self.set_char(player.holding.chr)
            player.holding.set_char(tmp)
        else:
            # Picks up a Letter from conveyor belt
            player.holding = self.clone()
            player.holding.interactable = 0
            player.holding.set_size(40)
            player.set_holding(state, True)
            player.update_holding_position()
            self.kill()
        return
    
    def fall(self):
        """
        Starts the falling animation when wrong answer is submitted
        """
        # 1. Start the falling process
        self.interactable = 0
        self.is_falling = True

        # 2. Adds a random amount of upward velocity to the letter
        self.vx = uniform(-20, 20)
        self.vy = -160 + uniform(-30, 30)

