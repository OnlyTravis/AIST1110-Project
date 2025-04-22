from pygame import key, event, KEYDOWN, K_e, K_w, K_a, K_s, K_d, K_UP, K_DOWN, K_LEFT, K_RIGHT
from pygame.event import Event

from src.classes.state import GameState
from src.sprites.player import Player

class HumanPlayer(Player):
    def __init__(self, x, y, is_p1):
        super().__init__(x, y, is_p1)
        
        # 1. Setup key binds
        if is_p1:
            self.key_set = [K_w, K_s, K_a, K_d]
        else:
            self.key_set = [K_UP, K_DOWN, K_LEFT, K_RIGHT]  # Local Multiplayer
        
        # 2. Setup listeners
        self.interact_next_frame = False
        self.add_event_listener(KEYDOWN, self._handle_key_down)
    
    def _handle_key_down(self, event: Event):
        if event.key == K_e:
            self.interact_next_frame = True
    
    def update(self, state: GameState, dt: float):
        # 1. Checks Key Presses
        keys = key.get_pressed()
        dir = [0, 0]
        if keys[self.key_set[0]]:
            dir[1] -= 1
        if keys[self.key_set[1]]:
            dir[1] += 1
        if keys[self.key_set[2]]:
            dir[0] -= 1
        if keys[self.key_set[3]]:
            dir[0] += 1
        self.walk(state, dir[0], dir[1], dt)

        # 2. Interact
        if self.interact_next_frame:
            if self.is_p1:
                if state.player1_near != None:
                    self.interact(state.player1_near)
            else: 
                if state.player2_near != None:
                    self.interact(state.player2_near)
            self.interact_next_frame = False