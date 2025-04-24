from collections.abc import Callable

from pygame import surface, KEYDOWN
from pygame.sprite import Group
from pygame.event import Event

from src.classes.game_manager import GameManager, GameEvent
from src.classes.game_object import GameObject
from src.classes.state import States, GameState, Gamemode
from src.classes.scene import Scene
from src.sprites.human_player import HumanPlayer
from src.sprites.conveyor import ConveyorBelt
from src.sprites.trash_can import TrashCan
from src.sprites.submit_area import SubmitArea
from src.ui_element.question_box import QuestionBox
from src.ui_element.timer import Timer
from src.constants import INTERACT_DISTANCE

class GameScreen(Scene):
    def __init__(self, screen: surface.Surface, toScene: Callable):
        super().__init__(screen, toScene)

        self.state = GameState()
        self.manager = GameManager()
        self._init_ui()
        self._init_objects()
        self._init_game_state()
        self.add_event_listener(KEYDOWN, self._handle_key_down)
        self.add_event_listener(GameEvent.GameStart, self._on_game_start)

    def _init_ui(self):
        w, h = self.screen.get_size()
        self.uis = Group()
        self.uis.add(QuestionBox(w/2, 110))
        self.uis.add(Timer(w-100, 110))

    def _init_objects(self):
        w, h = self.screen.get_size()
        self.objs = Group()
        self.objs.add(ConveyorBelt(w/2-400, 280, 300, False))
        self.objs.add(ConveyorBelt(w/2+400, 280, 300, False))
        self.objs.add(ConveyorBelt(w/2-375, 605, 340, True))
        self.objs.add(ConveyorBelt(w/2+40, 605, 340, True, False))
        self.objs.add(ConveyorBelt(w/2-25, 280, 300, False))
        self.objs.add(ConveyorBelt(w/2+25, 280, 300, False))
        self.objs.add(TrashCan(w/2-175, 430))
        self.objs.add(TrashCan(w/2+175, 430))
        self.objs.add(SubmitArea(w/2-200, 250, 200, True))
        self.objs.add(SubmitArea(w/2+200, 250, 200, False))

        self.player1 = HumanPlayer(w/2-100, h/2, True)
        self.player2 = HumanPlayer(w/2+100, h/2, False)

    def _init_game_state(self):
        self.state.player1_pos = (self.player1.x, self.player1.y)
        self.state.gamemode = Gamemode.LocalMultiplayer # Add change gamemode later

    def draw(self):
        self.screen.fill(color=(200,200,200))
        
        for obj in self.objs.sprites():
            obj.draw(self.screen, self.state)
        self.player1.draw(self.screen, self.state)
        self.player2.draw(self.screen, self.state)

        for ui in self.uis.sprites():
            ui.draw(self.screen, self.state)

    def update(self, dt):
        self._check_player_near(self.objs.sprites())

        for obj in self.objs.sprites():
            obj.update(self.state, dt)
        self.player1.update(self.state, dt)
        self.player2.update(self.state, dt)

        for ui in self.uis.sprites():
            ui.update(self.state, dt)
        
        self.manager.update(self.state, dt)
    
    def _handle_key_down(self, event: Event):
        """
        Handles KEYDOWN events (e.g. menu_open...)
        """
        pass

    def _on_game_start(self, event: Event):
        """
        Change GameState, Display first question
        """
        self.state.game_state = States.Playing

    def _check_player_near(self, objs):
        """
        Updates player1_near & player2_near state
        """
        self.state.player1_near = None
        self.state.player2_near = None

        def check_group(objs: list[GameObject]) -> list[tuple[float, GameObject]]:
            closest1 = (1e10, None)
            closest2 = (1e10, None)
            for obj in objs:
                if obj.recursive:
                    closest = check_group(obj.inner_objects.sprites())
                    if closest[0][0] < closest1[0]:
                        closest1 = closest[0]
                    if closest[1][0] < closest2[0]:
                        closest2 = closest[1]

                if obj.can_interact_with_p1:
                    d1 = obj.distance_to(self.state.player1_pos)
                    if d1 < closest1[0]:
                        closest1 = (d1, obj)

                if self.state.gamemode != Gamemode.LocalMultiplayer:
                    continue

                if obj.can_interact_with_p2:
                    d2 = obj.distance_to(self.state.player2_pos)
                    if d2 < closest2[0]:
                        closest2 = (d2, obj)
            return [closest1, closest2]
        
        closest1, closest2 = check_group(objs)
        if closest1[0] < INTERACT_DISTANCE:
            self.state.player1_near = closest1[1]
        if closest2[0] < INTERACT_DISTANCE:
            self.state.player2_near = closest2[1]
