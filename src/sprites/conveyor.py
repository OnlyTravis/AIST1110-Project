from pygame import draw, Rect
from pygame.surface import Surface

from src.classes.game_object import GameObject
from src.classes.state import GameState
from src.sprites.letter import Letter

LETTER_SEPARATION = 60

class ConveyorBelt(GameObject):
    def __init__(self, 
                 x: int,
                 y: int,
                 length: int,
                 is_horizontal: bool,
                 is_forward=True):
        super().__init__(x, y, 0, True)
        self.length: int = length
        self.rate: float = 1.5
        self.speed: int = 3
        self.is_horizontal = is_horizontal
        self.is_forward = is_forward
        self._animation_tick = 0
        self._time_since_new = 0
    
    def draw(self, screen: Surface, state: GameState):
        # 1.1 Draw Border
        if self.is_horizontal:
            draw.rect(screen, "black", Rect(self.x, self.y-25, self.length, 50))
            draw.rect(screen, "gray", Rect(self.x+5, self.y-20, self.length-10, 40))
        else:
            draw.rect(screen, "black", Rect(self.x-25, self.y, 50, self.length))
            draw.rect(screen, "gray", Rect(self.x-20, self.y+5, 40, self.length-10))
        
        # 1.2 Draw Conveyor segments
        l = 20*self._animation_tick
        if not self.is_forward:
            l = 20-l
        while abs(l) < self.length:
            if self.is_horizontal:
                draw.line(screen, "black", (self.x+l, self.y-20), (self.x+l, self.y+20))
            else:
                draw.line(screen, "black", (self.x-20, self.y+l), (self.x+20, self.y+l))
            l += 20
        
        # 2. Draw inner letters
        super().draw(screen, state)

    def update(self, state: GameState, dt: float):
        # 1. Update conveyor animation
        self._animation_tick += 0.01*self.speed
        if (self._animation_tick >= 1):
            self._animation_tick -= 1
        
        # 2. Move Letters on the conveyor belt
        dir = 2*self.is_forward-1
        dx = 0.2*self.speed*dir if self.is_horizontal else 0
        dy = 0 if self.is_horizontal else 0.2*self.speed*dir
        for letter in self.inner_objects.sprites():
            letter.move(dx, dy)

        # 3 Remove & Add Letter to belt
        self._check_letters()
        self._time_since_new += dt
        if self._time_since_new > self.rate:
            self._time_since_new -= self.rate
            self._add_letter()
        
        # 4. Update Letter
        for letter in self.inner_objects.sprites():
            letter.update(state, dt)
    
    def _add_letter(self):
        x = self.x + self.length if self.is_horizontal and not self.is_forward else self.x
        y = self.y + self.length if not self.is_horizontal and not self.is_forward else self.y
        new_letter = Letter.random(x, y)
        self.inner_objects.add(new_letter)

    def _check_letters(self):
        letters: list[Letter] = self.inner_objects.sprites()

        if len(letters) == 0:
            return
        
        first = letters[0]
        if (self.is_forward):
            if (self.is_horizontal):
                if (first.x > self.x + self.length):
                    first.kill()
            else:
                if (first.y > self.y + self.length):
                    first.kill()
        else:
            if (self.is_horizontal):
                if (first.x < self.x):
                    first.kill()
            else:
                if (first.y < self.y):
                    first.kill()