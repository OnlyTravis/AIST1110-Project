from typing import Callable
from pygame.event import Event, EventType
from pygame.sprite import Sprite, Group
from pygame.surface import Surface

from src.classes.event import event_handler, GameEvent
from src.classes.state import GameState

class UIElement(Sprite):
    def __init__(self,
                x: float,
                y: float,
                recursive=False):
        super().__init__()
        self.x = x
        self.y = y
        self.recursive = recursive
        self.inner_elements = Group()
        self.listeners: list[int] = []
    
    def draw(self, screen: Surface, state: GameState):
        if self.recursive:
            for obj in self.inner_elements.sprites():
                obj.draw(screen, state)

    def update(self, state: GameState, dt: float):
        if self.recursive:
            for obj in self.inner_elements.sprites():
                obj.update(state, dt)

    def add_inner_element(self, ele: "UIElement"):
        assert self.recursive
        self.inner_elements.add(ele)

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