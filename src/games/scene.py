from collections.abc import Callable

from src.games.event import event_handler

class Scene():
    def __init__(self, toScene: Callable):
        self.toScene: Callable = toScene
        self.listeners: list[int] = []
    
    def update():
        pass

    def draw():
        pass

    def exit(self):
        for listener_id in self.listeners:
            event_handler.removeListener(listener_id)

    def exitTo(self, scene):
        self.exit()
        self.toScene(scene)