from pygame import font
from pygame.surface import Surface

from src.classes.game_object import GameObject
from src.classes.state import GameState

class Timer(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y) #, "0:00", "red", 40, TextAlign.Center
        self.current: int = 0
        self.font = font.Font(font.get_default_font(), 45)
        self._update_display()

    def draw(self, screen: Surface, state: GameState):
        screen.blit(self.rendered_text, self.text_rect)

    def update(self, state: GameState, dt):
        if self.current != int(state.timer):
            self.current = int(state.timer)
            self._update_display()

    def _update_display(self):
        m = self.current // 60
        s = self.current % 60
        self.rendered_text = self.font.render(f"{m}:{s:0>2}", True, "red")
        self.text_rect = self.rendered_text.get_rect(center=(self.x, self.y))