from collections.abc import Callable
from pygame import surface
from pygame.sprite import Group

from src.games.scene import Scene
from src.sprites.letter import Letter

class GameScene(Scene):
    def __init__(self, screen: surface.Surface, toScene: Callable):
        super().__init__(screen, toScene)

        self.init_objects()

    def init_objects(self):
        self.objs = Group()
        self.objs.add(Letter("A", 100, 200))

    def draw(self):
        self.screen.fill("white")
        
        for obj in self.objs.sprites():
            obj.draw(self.screen)

    
    def update(self):
        pass