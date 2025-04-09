from collections.abc import Callable
from pygame.surface import Surface

from src.games.event import event_handler

class Scene():
    def __init__(self, screen: Surface, toScene: Callable):
        self.screen = screen
        self.toScene: Callable = toScene
        self.listeners: list[int] = []
    
    def update(self):
        pass

    def draw(self):
        pass

    def exit(self):
        for listener_id in self.listeners:
            event_handler.removeListener(listener_id)

    def exitTo(self, scene_class):
        self.exit()
        self.toScene(scene_class)