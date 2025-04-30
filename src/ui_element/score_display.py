from src.classes.event import GameEvent
from src.classes.images import ImageLoader, Images
from src.classes.ui_element import UIElement
from src.ui_element.text import Text, TextAlign

BOUNDARIES = [0, 30, 60, 110, 150, 200, 250]

class ScoreDisplay(UIElement):
    def __init__(self, 
                 x: float,
                 y: float,
                 is_p1: bool=True):
        super().__init__(x, y)

        self.size = 200
        self.is_p1 = is_p1
        self.index = 0

        text_color = "#ff5252" if is_p1 else "#7ebbfc"
        self.text = Text(x+0.1*self.size, y+0.38*self.size, "0", text_color, 35, TextAlign.Start)
        frame_indices = [x for x in range(8)] if is_p1 else [x+8 for x in range(8)]
        self.frames = ImageLoader.get_frames(Images.ScoreDisplay, 64, self.size, self.size, frame_indices)

        self.add_event_listener(GameEvent.SubmitStatus, self._on_submit)

    def _on_submit(self, event):
        new_score = event.p1_score if self.is_p1 else event.p2_score

        for i, value in enumerate(BOUNDARIES):
            if new_score <= value:
                self.index = i
                break
        else:
            i += 1

        self.text.set_text(str(new_score))

    def draw(self, screen):
        pos = (self.x-self.size/2, self.y-self.size/2)
        screen.blit(self.frames[self.index], pos)
        self.text.draw(screen)
        super().draw(screen)
    
    def update(self, dt):
        super().update(dt)