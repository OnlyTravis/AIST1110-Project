from collections.abc import Callable
from pygame.sprite import Group
from pygame.event import Event
from pygame import surface, key, KEYDOWN, K_w, K_a, K_s, K_d, K_e

from src.sprites.conveyor import ConveyorBelt
from src.classes.state import GameState, Gamemode
from src.classes.scene import Scene
from src.sprites.letter import Letter
from src.sprites.human_player import HumanPlayer

class GameScreen(Scene):
    def __init__(self, screen: surface.Surface, toScene: Callable):
        super().__init__(screen, toScene)

        self.state = GameState()
        self._init_objects()
        self._init_game_state()
        self.add_event_listener(KEYDOWN, self._handle_key_down)

    def _init_objects(self):
        self.objs = Group()
        self.objs.add(ConveyorBelt(100, 100, 300, False))
        self.player1 = HumanPlayer(400, 400, True)

    def _init_game_state(self):
        self.state.player1_pos = (self.player1.x, self.player1.y)
        self.state.gamemode = Gamemode.SinglePlayer # Add change gamemode later

    def _handle_key_down(self, event: Event):
        """
        Handles KEYDOWN events (e.g. interact, menu_open...)
        """
        if event.key == K_e:
            self.player1.check_interact(self.objs.sprites())

    def draw(self):
        self.screen.fill("white")
        
        for obj in self.objs.sprites():
            obj.draw(self.screen)
        self.player1.draw(self.screen)

    def update(self, dt):
        # Reset near state
        self.state.player1_near = None
        self.state.player2_near = None

        for obj in self.objs.sprites():
            obj.update(self.state, dt)
        self.player1.update(self.state, dt)