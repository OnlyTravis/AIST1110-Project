from pygame.surface import Surface

from src.ui_element.text import Text, TextAlign

class Annouce(Text):
    def __init__(self, 
                 x: float,
                 y: float,
                 text: str,
                 duration: float = 1.5,
                 fade_duration: float = 0.5,
                 color="black",
                 font_size = 30,
                 align=TextAlign.Center):
        """
        duration: seconds before the text completely disappears
        fade_duration: the duration of the fading animation
        """
        super().__init__(x, y, text, color, font_size, align)
        self.fade_duration = fade_duration
        self.timer = duration
    
    def draw(self, screen):
        if self.timer >= self.fade_duration:
            super().draw(screen)
        else:
            self.rendered_text.set_alpha(int(255*self.timer/self.fade_duration))
            super().draw(screen)

    def update(self, dt):
        super().update(dt)
        self.timer -= dt
        if self.timer < 0:
            self.kill()
