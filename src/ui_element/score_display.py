
from src.classes.event import GameEvent
from src.ui_element.text import Text, TextAlign

class ScoreDisplay(Text):
    def __init__(self, 
                 x: float,
                 y: float,
                 is_p1: bool=True):
        super().__init__(x, y, "Score: 0", "red", 30, TextAlign.Center)
        self.is_p1 = is_p1
        self.add_event_listener(GameEvent.SubmitStatus, self._on_submit)

    def _on_submit(self, event):
        new_score = event.p1_score if self.is_p1 else event.p2_score
        self.set_text(f"Score: {new_score}")

    def draw(self, screen):
        super().draw(screen)
    
    def update(self, dt):
        super().update(dt)