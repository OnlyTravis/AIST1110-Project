from collections.abc import Callable
from enum import Enum
from pygame.sprite import Group
from pygame.surface import Surface

from src.classes.event import EventListener
from src.classes.ui_element import UIElement

class Scenes(Enum):
    TitleScreen = 0
    OptionScreen = 1
    TutorialScreen = 2
    GameScreen = 3

class Scene(EventListener):
    def __init__(self, screen: Surface, to_scene: Callable):
        self.screen: Surface = screen
        self.to_scene: Callable = to_scene
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

    def exit_to(self, scene: Scenes, **args):
        self.exit()
        self.to_scene(scene, **args)