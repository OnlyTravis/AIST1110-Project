from pygame.surface import Surface
from pygame import draw, Vector2

from src.classes.state import GameState
from src.classes.game_object import GameObject
from src.sprites.trash_can import TrashCan
from src.sprites.letter import Letter

class Player(GameObject):
    def __init__(self, x: float, y: float, is_p1: bool):
        super().__init__(x, y, False)
        self.speed: float = 300
        self.is_p1: bool = is_p1
        self.is_holding: bool = False
        self.holding: Letter = None
    
    def draw(self, screen: Surface, state: GameState):
        # 1. Draw Player
        draw.circle(screen, "red", (self.x, self.y), 10)

        # 2. Draw Holding Object
        if self.holding != None:
            self.holding.draw(screen, state)
    
    def walk(self, state: GameState, x_dir: int, y_dir: int, dt: float):
        """
        Allows player to walk in a certain direction.
        x_dir (-1 : left) (0 : standing) (1 : right)
        y_dir (-1 : up)   (0 : standing) (1 : down)
        """
        # 1. Moves Player & Holding
        if x_dir == 0 and y_dir == 0:
            return
        vec = Vector2(x_dir, y_dir)
        vec.scale_to_length(self.speed * dt)
        self.move(vec.x, vec.y)
        
        if self.is_holding:
            self.holding.move_to(self.x, self.y)

        # 2. Update Game State
        if self.is_p1:
            state.player1_pos = self.pos
        else:
            state.player2_pos = self.pos
    
    def interact(self, obj: GameObject):
        """
        Interacts with a interactable object
        (e.g. Picking up a Letter, Trashing holding Letter...)
        """
        if isinstance(obj, Letter):
            if self.is_holding:
                # Swap Holding with the one on conveyor belt
                tmp = obj.chr
                obj.set_char(self.holding.chr)
                self.holding.set_char(tmp)
            else:
                # Picks up a Letter from conveyor belt
                self.holding = obj.clone()
                self.holding.interactable = False
                self.holding.set_size(40)
                self.is_holding = True
                obj.kill()
            return
        
        if isinstance(obj, TrashCan):
            if not self.is_holding:
                return
            
            self.holding.kill()
            self.holding = None
            self.is_holding = False
        
