from pygame import draw, Rect
from pygame.surface import Surface
from pygame.sprite import Group

from src.classes.game_object import GameObject
from src.classes.state import GameState
from src.sprites.letter import Letter

class ConveyorBelt(GameObject):
    def __init__(self, 
                 x: int,
                 y: int,
                 length: int,
                 is_horizontal: bool):
        super().__init__(x, y, False)
        self.length: int = length
        self.speed: int = 3
        self.is_horizontal = is_horizontal
        self.letters = Group()
        self._animation_tick = 0
    
    def draw(self, screen: Surface):
        # 1. Draw Border
        if self.is_horizontal:
            draw.rect(screen, "black", Rect(self.x, self.y-25, self.length, 50))
            draw.rect(screen, "gray", Rect(self.x+5, self.y-20, self.length-10, 40))
        else:
            draw.rect(screen, "black", Rect(self.x-25, self.y, 50, self.length))
            draw.rect(screen, "gray", Rect(self.x-20, self.y+5, 40, self.length-10))
        
        # 2. Draw Conveyor segments
        l = 20*self._animation_tick
        while l < self.length:
            if self.is_horizontal:
                draw.line(screen, "black", (self.x+l, self.y-20), (self.x+l, self.y+20))
            else:
                draw.line(screen, "black", (self.x-20, self.y+l), (self.x+20, self.y+l))
            l += 20
        
        # 3. Draw Letters
        for letter in self.letters.sprites():
            letter.draw(screen)

    def update(self, state: GameState, dt: float):
        # 1. Update conveyor movement
        self._animation_tick += 0.01*self.speed
        if (self._animation_tick >= 1):
            self._animation_tick -= 1
        
        # 2. Move Letters on the belt
        dx = 0.2*self.speed if self.is_horizontal else 0
        dy = 0 if self.is_horizontal else 0.2*self.speed
        for letter in self.letters:
            letter.move(dx, dy)

        # 3. Add / Remove Letters on belt
        if self.is_horizontal:
            if (len(self.letters) > 0) and (self.letters.sprites()[0].x > self.x+self.length):
                self.letters.sprites()[0].kill()
            if (len(self.letters) == 0) or (self.letters.sprites()[len(self.letters) - 1].x > self.x + 50):
                self.letters.add(Letter.random(self.x, self.y))
        else:
            if (len(self.letters) > 0) and (self.letters.sprites()[0].y > self.y+self.length):
                self.letters.sprites()[0].kill()
            if (len(self.letters) == 0) or (self.letters.sprites()[len(self.letters) - 1].y > self.y + 50):
                self.letters.add(Letter.random(self.x, self.y))
        
        # 4. Update Letter
        for letter in self.letters.sprites():
            letter.update(state, dt)
