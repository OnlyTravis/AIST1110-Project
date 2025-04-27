from collections.abc import Callable
from pygame.sprite import Group
from pygame.surface import Surface

from src.classes.event import EventListener
from src.classes.ui_element import UIElement

class Scene(EventListener):
    def __init__(self, screen: Surface, toScene: Callable):
        self.screen: Surface = screen
        self.toScene: Callable = toScene
        self.listeners: list[int] = []
        self._ui_elements = Group()
    
    def add_element(self, ele: UIElement):
        self._ui_elements.add(ele)
    
    def update(self, dt):
        self._ui_elements.update(dt=dt)

    def draw(self):
        for ele in self._ui_elements.sprites():
            ele.draw(self.screen)

    def exit(self):
        self.remove_all_listeners()
        for ele in self._ui_elements.sprites():
            ele.kill()

    def exitTo(self, scene_class):
        self.exit()
        self.toScene(scene_class)