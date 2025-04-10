from collections.abc import Callable
from typing import Self
from math import dist
from pygame.sprite import Sprite
from pygame.event import Event, EventType

from src.classes.state import GameState
from src.classes.event import event_handler

class GameObject(Sprite):
    def __init__(self, x, y, interactable: bool):
        super().__init__()
        self.listeners: list[int] = []
        self.x = x
        self.y = y
        self.interactable = interactable

    def draw(self):
        pass

    def update(self, state: GameState, dt: float):
        pass

    def move(self, dx: float, dy: float):
        """
        Moves GameObject by a certain amount (dx, dy)
        """
        self.x += dx
        self.y += dy
    
    def move_to(self, x: float, y: float):
        """
        Moves GameObject to a certain location
        """
        self.x = x
        self.y = y
    
    def distance_to(self, pos: tuple) -> float:
        """
        Returns the distance between self and a coordinate
        """
        return dist((self.x, self.y), pos)

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
    
    @property
    def pos(self):
        return (self.x, self.y)

    @pos.setter
    def pos(self, new_pos):
        self.x = new_pos[0]
        self.y = new_pos[1]
