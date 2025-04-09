from collections.abc import Callable
from pygame import KEYDOWN, K_SPACE, event, surface, font

from src.games.scene import Scene
from src.games.event import event_handler
from src.scenes.tutorial import TutorialScreen

class TitleScreen(Scene):
    def __init__(self, screen: surface.Surface, toScene: Callable):
        super().__init__(toScene)

        self.screen = screen

        listener_id = event_handler.addListener(KEYDOWN, self.onKeyDown)
        self.listeners.append(listener_id)

        # Init texts
        font_1 = font.Font(font.get_default_font(), 40)
        self.title = font_1.render("Title Screen", True, "black")
        self.tip =  font_1.render("Press Space to Start", True, "black")
        self.tip_position = 0
        self.tip_velocity = 0
        self.tip_direction = 1

    def draw(self):
        w, h = self.screen.get_size()

        # Draw texts
        self.screen.fill("gray")
        title_rect = self.title.get_rect(center=(w/2, h/2))
        self.screen.blit(self.title, title_rect)
        tip_rect = self.tip.get_rect(center=(w/2, h/2+130+self.tip_position))
        self.screen.blit(self.tip, tip_rect)
    
    def update(self):
        self.tip_velocity += self.tip_direction*0.05
        self.tip_position += self.tip_velocity
        if self.tip_position > 10:
            self.tip_direction = -1
        elif self.tip_position < 0:
            self.tip_direction = 1 

    def onKeyDown(self, event: event.Event):
        print(event)
        if event.key == K_SPACE:
            self.exitTo(TutorialScreen)