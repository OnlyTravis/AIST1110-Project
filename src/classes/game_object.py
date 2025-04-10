from collections.abc import Callable
from pygame.sprite import Sprite
from pygame.event import Event, EventType

from src.classes.event import event_handler

class GameObject(Sprite):
    def __init__(self):
        super().__init__()
        self.listeners: list[int] = []

    def draw(self):
        pass

    def update(self, dt):
        pass

    def add_event_listener(self, event_type: EventType, func: Callable[[Event], None]):
        listener_id = event_handler.add_listener(event_type, func)
        self.listeners.append(listener_id)
    
    def remove_event_listener(self, listener_id: int):
        self.listeners.remove(listener_id)
        event_handler.remove_listener(listener_id)
    
    def kill(self):
        for listener_id in self.listeners:
            event_handler.remove_listener(listener_id)
        super().kill()