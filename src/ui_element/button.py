from typing import Callable
from pygame import draw, mouse, Rect, MOUSEBUTTONDOWN, color
from pygame.color import Color
from pygame.surface import Surface

from src.classes.ui_element import UIElement

class Button(UIElement):
    """
    A Base Class For All UI Buttons
    """
    def __init__(self, 
                 x: float,
                 y: float,
                 w: float,
                 h: float,
                 on_click: Callable,
                 background_color = Color(200, 200, 200),
                 border_radius: int=0):
        """
        background_color = None : No Background
        """
        super().__init__(x, y)
        self.w = w
        self.h = h
        self.rect = Rect(self.x-self.w/2, self.y-self.h/2, 
                         self.w, self.h)
        self.background_color = background_color
        self.hover_color = Color(
            int(255-(255-background_color.r)*0.8),
            int(255-(255-background_color.g)*0.8),
            int(255-(255-background_color.b)*0.8)
        )
        self.border_radius = border_radius
        self.is_hover = False
        self.on_click = on_click
        self.add_event_listener(MOUSEBUTTONDOWN, self._on_click)
    
    def draw(self, screen: Surface):
        if self.is_hover:
            draw.rect(screen, self.hover_color, self.rect, 0, self.border_radius)
        else:
            draw.rect(screen, self.background_color, self.rect, 0, self.border_radius)

    def update(self, dt: float):
        mouse_pos = mouse.get_pos()
        self.is_hover = self.rect.collidepoint(mouse_pos)

    def _on_click(self, event):
        """
        Listening to on click Event
        """
        if self.is_hover:
            self.on_click()