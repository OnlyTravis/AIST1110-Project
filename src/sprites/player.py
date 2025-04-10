from pygame.surface import Surface
from pygame import draw, Vector2

from src.classes.game_object import GameObject

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y
        self.speed = 300
    
    def draw(self, screen: Surface):
        draw.circle(screen, "red", (self.x, self.y), 10)
    
    def move(self, dx: float, dy: float):
        """
        Allows Game Objects (e.g. Conveyor belt) to move players
        """
        self.x += dx
        self.y += dy
    
    def walk(self, x_dir: int, y_dir: int, dt: float):
        """
        Allows player to walk in a certain direction.
        x_dir (-1 : left) (0 : standing) (1 : right)
        y_dir (-1 : up)   (0 : standing) (1 : down)
        """
        if x_dir == 0 and y_dir == 0:
            return
        
        vec = Vector2(x_dir, y_dir)
        vec.scale_to_length(self.speed * dt)
        self.move(vec.x, vec.y)

