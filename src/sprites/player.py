from pygame import draw, Vector2, SRCALPHA
from pygame.surface import Surface

from src.classes.state import GameState
from src.classes.images import ImageLoader, Images
from src.classes.game_object import GameObject
from src.sprites.letter import Letter

class Player(GameObject):
    def __init__(self, 
                 x: float,
                 y: float,
                 is_p1: bool,
                 movable_area: tuple):
        super().__init__(x, y, 0)
        self.speed: float = 500
        self.is_p1: bool = is_p1
        self.is_holding: bool = False
        self.holding: Letter = None
        self.movable_area = movable_area

        indices = [x for x in range(8)] if is_p1 else [x+8 for x in range(8)]
        self.size = 60
        self.frames = ImageLoader.get_frames(Images.Player, 64, self.size, self.size, indices)
        self.index = 0
        self.glow = Surface((self.size, self.size), flags=SRCALPHA)
        draw.circle(self.glow, "#ffeda6", (self.size/2, self.size/2), self.size/2)
        self.glow.set_alpha(50)
    
    def draw(self, screen: Surface, state: GameState):
        # 1. Draw Player
        is_holding = 4 if self.is_holding else 0
        pos = (self.x-self.size/2, self.y-self.size/2)
        screen.blit(self.glow, pos)
        screen.blit(self.frames[self.index+is_holding], pos)

        # 2. Draw Holding Object
        if self.holding != None:
            self.holding.draw(screen, state)
    
    def walk(self, state: GameState, x_dir: int, y_dir: int, dt: float):
        """
        Allows player to walk in a certain direction.
        x_dir (-1 : left) (0 : standing) (1 : right)
        y_dir (-1 : up)   (0 : standing) (1 : down)
        """
        # 1. Moves Player change frame index
        if x_dir == 0 and y_dir == 0:
            return
        vec = Vector2(x_dir, y_dir)
        vec.scale_to_length(self.speed * dt)
        self.move(vec.x, vec.y)
        self.index = 1 if y_dir == 0 else 0 if y_dir == 1 else 3
        if self.index == 1 and x_dir == -1:
            self.index = 2
        
        # 2. Check collision with wall & Move holding position
        if self.x < self.movable_area[0]:
            self.move_to(self.movable_area[0], self.y)
        elif self.x > self.movable_area[2]:
            self.move_to(self.movable_area[2], self.y)
        if self.y < self.movable_area[1]:
            self.move_to(self.x, self.movable_area[1])
        elif self.y > self.movable_area[3]:
            self.move_to(self.x, self.movable_area[3])
        self.update_holding_position()

        # 3. Update Game State
        if self.is_p1:
            state.player1_pos = self.pos
        else:
            state.player2_pos = self.pos
    
    def update_holding_position(self):
        if self.is_holding:
            self.holding.move_to(self.x, self.y-self.size/2)

    def set_holding(self, state: GameState, is_holding: bool):
        if self.is_holding == is_holding:
            return

        if not is_holding:
            self.holding.kill()
            self.holding = None

        self.is_holding = is_holding

        if self.is_p1:
            state.player1_is_holding = is_holding
        else:
            state.player2_is_holding = is_holding
    
    def interact(self, state: GameState, obj: GameObject):
        """
        Interacts with a interactable object
        (e.g. Picking up a Letter, Trashing holding Letter...)
        """
        obj.on_interact(self, state)   
