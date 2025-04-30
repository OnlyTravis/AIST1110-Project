from pygame.sprite import Sprite, Group
from pygame.surface import Surface

from src.classes.event import EventListener

class UIElement(Sprite, EventListener):
    def __init__(self,
                x: float,
                y: float,
                recursive=False):
        Sprite.__init__(self)
        EventListener.__init__(self)
        self.x = x
        self.y = y
        self.recursive = recursive
        self.inner_elements = Group()
    
    def draw(self, screen: Surface):
        if self.recursive:
            for obj in self.inner_elements.sprites():
                obj.draw(screen)

    def update(self, dt: float):
        if self.recursive:
            for obj in self.inner_elements.sprites():
                obj.update(dt)

    def add_inner_element(self, ele: "UIElement"):
        assert self.recursive
        self.inner_elements.add(ele)

    def kill(self):
        self.remove_all_listeners()
        if self.recursive:
            for obj in self.inner_elements.sprites():
                obj.kill()
        super().kill()

    def get_pos(self, offset: tuple[float, float]) -> tuple[float, float]:
        return (self.x + offset[0], self.y + offset[1])

    @property
    def pos(self):
        return (self.x, self.y)

    @pos.setter
    def pos(self, new_pos: tuple[float, float]):
        self.x = new_pos[0]
        self.y = new_pos[1]