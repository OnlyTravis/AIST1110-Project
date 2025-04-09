import pygame.event
from collections.abc import Callable

from src.general.singleton import Singleton

class EventListener():
    def __init__(self, id: int, func: Callable):
        self.id = id
        self.func = func
    
    def run(self, event: pygame.event.Event):
        self.func(event)

class EventHandler(metaclass=Singleton):
    def __init__(self):
        self.listeners: dict[int, list[EventListener]] = {}
        self.id_counter = 0

    def handle_event(self, event: pygame.event.Event):
        if not event.type in self.listeners.keys():
            return
        
        for listener in self.listeners[event.type]:
            listener.run(event)

    def addListener(self, event_type: int, func: Callable) -> int:
        arr = self.listeners.setdefault(event_type, [])
        arr.append(EventListener(self.id_counter, func))
        self.id_counter += 1
        return self.id_counter - 1
    
    def removeListener(self, listenerId) -> bool:
        """
        Removes Event Listener With Given Id

        Returns True if successfully removed
        Returns False if listener not found
        """
        for listener_arr in self.listeners.values():
            for listener in listener_arr:
                if listener.id == listenerId:
                    listener_arr.remove(listener)
                    return True
        return False