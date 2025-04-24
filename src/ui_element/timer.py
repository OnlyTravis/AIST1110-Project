from src.ui_element.text import Text, TextAlign

class Timer(Text):
    def __init__(self, x, y):
        super().__init__(x, y, "0:00", "red", 40, TextAlign.Center)
        self.current: int = 0

    def draw(self, screen, state):
        super().draw(screen, state)

    def update(self, state, dt):
        if self.current != int(state.timer):
            self.current = int(state.timer)
            self._update_display()
        super().update(state, dt)

    def _update_display(self):
        m = self.current // 60
        s = self.current % 60
        self.set_text(f"{m}:{s:0>2}")