from collections.abc import Callable
from math import dist
from pygame.sprite import Sprite, Group
from pygame.event import Event, EventType

from src.classes.state import GameState
from src.classes.event import event_handler, GameEvent

class GameObject(Sprite):
    def __init__(self, 
                 x, 
                 y, 
                 interactable=0,
                 recursive=False):
        """
        interactable: (0: not interactable), (1: p1), (2: p2), (3: p1 & p2)
        recursive: Object contains other objects
        """
        super().__init__()
        self.listeners: list[int] = []
        self.x = x
        self.y = y
        self.interactable = interactable
        self.recursive = recursive
        self.inner_objects = Group()

    def draw(self, screen, state):
        if self.recursive:
            for obj in self.inner_objects.sprites():
                obj.draw(screen, state)

    def update(self, state, dt):
        if self.recursive:
            for obj in self.inner_objects.sprites():
                obj.update(state, dt)

    def on_interact(self, player, state: GameState):
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

    def add_event_listener(self, event_type: EventType | GameEvent, func: Callable[[Event], None]):
        listener_id = event_handler.add_listener(event_type, func)
        self.listeners.append(listener_id)
    
    def remove_event_listener(self, listener_id: int):
        self.listeners.remove(listener_id)
        event_handler.remove_listener(listener_id)
    
    def kill(self):
        for listener_id in self.listeners:
            event_handler.remove_listener(listener_id)
        if self.recursive:
            for obj in self.inner_objects.sprites():
                obj.kill()
        super().kill()
    
    @property
    def pos(self):
        return (self.x, self.y)

    @pos.setter
    def pos(self, new_pos: tuple[float, float]):
        self.x = new_pos[0]
        self.y = new_pos[1]

    @property
    def can_interact_with_p1(self):
        return self.interactable == 1 or self.interactable == 3
    
    @property
    def can_interact_with_p2(self):
        return self.interactable == 2 or self.interactable == 3