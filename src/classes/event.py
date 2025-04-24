from enum import Enum
from collections.abc import Callable

from pygame import USEREVENT, event, time
from pygame.event import Event, EventType

class GameEvent(Enum):
    GameStart = USEREVENT
    UpdateQuestion = USEREVENT+1
    GameEnd = USEREVENT+2

    @classmethod
    def post(cls, game_event: "GameEvent", dict: dict={}):
        event.post(Event(game_event.value, **dict))

    @classmethod
    def set_timeout(cls, game_event: "GameEvent", miliseconds: int):
        time.set_timer(game_event.value, miliseconds, 1)

class EventListener():
    def __init__(self, id: int, func: Callable):
        self.id = id
        self.func = func
    
    def run(self, event: Event):
        self.func(event)

class EventHandler():
    def __init__(self):
        self.listeners: dict[int, list[EventListener]] = {}
        self.id_counter = 0

    def handle_event(self, event: Event):
        if not event.type in self.listeners.keys():
            return
        
        for listener in self.listeners[event.type]:
            listener.run(event)

    def add_listener(self, event_type: EventType | GameEvent, func: Callable[[Event], None]) -> int:
        if isinstance(event_type, GameEvent):
            event_type = event_type.value

        arr = self.listeners.setdefault(event_type, [])
        arr.append(EventListener(self.id_counter, func))
        self.id_counter += 1
        return self.id_counter - 1
    
    def remove_listener(self, listener_id) -> bool:
        """
        Removes Event Listener With Given Id

        Returns True if successfully removed
        Returns False if listener not found
        """
        for listener_arr in self.listeners.values():
            for listener in listener_arr:
                if listener.id == listener_id:
                    listener_arr.remove(listener)
                    return True
        return False

event_handler = EventHandler()