from pygame import draw, SRCALPHA, font
from pygame.surface import Surface

from src.classes.ui_element import UIElement

class ResultDisplay(UIElement):
    def __init__(self, x, y, is_correct, size=100):
        super().__init__(x, y)
        self.size = size
        self.fade_time = 1.2
        self.timer = self.fade_time
        self._init_display(is_correct)

    def _init_display(self, is_correct: bool):
        self.symbol = Surface((self.size, self.size), SRCALPHA)
        self.symbol.convert_alpha()
        text_font = font.Font(font.get_default_font(), int(self.size/3))

        if is_correct:
            dots = [
                (0, self.size/2), 
                (self.size/2, self.size),
                (self.size, 0)
            ]
            draw.lines(self.symbol, "lime", False, dots, 8)
            self.rendered_text = text_font.render("Correct", True, "lime")
        else:
            draw.line(self.symbol, "red", (0, 0), (self.size, self.size), 8)
            draw.line(self.symbol, "red", (0, self.size), (self.size, 0), 8)
            self.rendered_text = text_font.render("Incorrect", True, "red")
        self.text_rect = self.rendered_text.get_rect(center=self.get_pos((0, self.size)))
    
    def draw(self, screen):
        alpha = int((self.timer/self.fade_time)*255)
        self.symbol.set_alpha(alpha)
        self.rendered_text.set_alpha(alpha)
        screen.blit(self.symbol, (self.x-self.size/2, self.y-self.size/2))
        screen.blit(self.rendered_text, self.text_rect)

    def update(self, dt):
        self.timer -= dt
        if self.timer < 0:
            self.kill()
            return