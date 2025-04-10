from collections.abc import Callable
from pygame.surface import Surface
from pygame.event import Event, EventType

from src.classes.event import event_handler

class Scene():
    def __init__(self, screen: Surface, toScene: Callable):
        self.screen = screen
        self.toScene: Callable = toScene
        self.listeners: list[int] = []
    
    def update(self, dt):
        pass

    def draw(self):
        pass

    def add_event_listener(self, event_type: EventType, func: Callable[[Event], None]):
        listener_id = event_handler.add_listener(event_type, func)
        self.listeners.append(listener_id)

    def exit(self):
        for listener_id in self.listeners:
            event_handler.remove_listener(listener_id)

    def exitTo(self, scene_class):
        self.exit()
        self.toScene(scene_class)