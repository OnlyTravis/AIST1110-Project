from pygame import draw
from pygame.surface import Surface

from src.classes.ui_element import UIElement
from src.classes.images import Images, ImageLoader

class Image(UIElement):
    def __init__(self, 
                 x: float,
                 y: float,
                 w: int,
                 h: int,
                 img: Images):
        super().__init__(x, y)
        self.w = w
        self.h = h
        self.img = ImageLoader.get(img, w, h)
    
    def draw(self, screen: Surface):
        screen.blit(self.img, (self.x-self.w/2, self.y-self.h/2))