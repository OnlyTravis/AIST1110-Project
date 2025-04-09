from collections.abc import Callable
from pygame import K_DOWN, K_SPACE, event

from src.games.scene import Scene
from src.games.event import event_handler
from src.scenes.tutorial import TutorialScreen

class TitleScreen(Scene):
    def __init__(self, screen, toScene: Callable):
        super().__init__(toScene)

        self.screen = screen

        listener_id = event_handler.addListener(K_DOWN, self.onKeyDown)
        self.listeners.append(listener_id)

    def draw():
        pass

    def onKeyDown(self, event: event.Event):
        if event.key == K_SPACE:
            self.exitTo(TutorialScreen())