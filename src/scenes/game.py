from collections.abc import Callable
from pygame.sprite import Group
from pygame.event import Event
from pygame import surface, KEYDOWN, K_e

from src.classes.scene import Scene
from src.sprites.letter import Letter
from src.sprites.human_player import HumanPlayer

class GameScreen(Scene):
    def __init__(self, screen: surface.Surface, toScene: Callable):
        super().__init__(screen, toScene)

        self._init_objects()
        self.add_event_listener(KEYDOWN, self._handle_key_press)

    def _init_objects(self):
        self.objs = Group()
        self.objs.add(Letter("A", 100, 200))
        self.player1 = HumanPlayer(400, 400)

    def _handle_key_press(self, event: Event):
        if event.key == K_e:
            self._check_action()

    def _check_action(self):
        pass

    def draw(self):
        self.screen.fill("white")
        
        for obj in self.objs.sprites():
            obj.draw(self.screen)
        self.player1.draw(self.screen)

    def update(self, dt):
        self.player1.update(dt)