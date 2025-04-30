from pygame import draw, transform, Rect
from pygame.surface import Surface

from src.classes.game_object import GameObject
from src.classes.event import GameEvent
from src.classes.images import ImageLoader, Images
from src.classes.state import GameState
from src.classes.data_classes import Question
from src.sprites.letter import Letter

SEPARATION = 30

class ConveyorBelt(GameObject):
    def __init__(self, 
                 x: int,
                 y: int,
                 length: int,
                 is_horizontal: bool,
                 is_forward=True):
        super().__init__(x, y, 0, True)

        self.length: int = length
        self.rate: float = 0.6
        self.speed: int = 100
        self.is_horizontal = is_horizontal
        self.is_forward = is_forward

        self._animation_tick = 0
        self._time_since_new = 0

        self.head = ImageLoader.get(Images.ConveyorHead, 80, 80)
        if self.is_horizontal:
            self.head = transform.rotate(self.head, 90)
        self.tail = transform.flip(self.head, True, True)

        self.answer_list: list[str] = []
        self.add_event_listener(GameEvent.UpdateQuestion, self.update_answer_list)
    
    def draw(self, screen: Surface, state: GameState):
        # 1.1 Draw Border
        if self.is_horizontal:
            draw.rect(screen, "black", Rect(self.x+25, self.y-40, self.length-50, 80))
            draw.rect(screen, "gray", Rect(self.x+25, self.y-30, self.length-50, 60))
        else:
            draw.rect(screen, "black", Rect(self.x-40, self.y+25, 80, self.length-50))
            draw.rect(screen, "gray", Rect(self.x-30, self.y+25, 60, self.length-50))
        
        # 1.2 Draw Conveyor segments
        l = 25+SEPARATION*self._animation_tick
        if not self.is_forward:
            l = 50+SEPARATION-l
        while abs(l)+SEPARATION < self.length:
            if self.is_horizontal:
                x, y = self.x + l, self.y
                draw.line(screen, "black", (x, y-20), (x, y+20))
                x += SEPARATION/2
                if self.is_forward:
                    draw.polygon(screen, (50, 50, 50), [(x-5, y-10), (x-5, y+10), (x+5, y)])
                else:
                    draw.polygon(screen, (50, 50, 50), [(x+5, y-10), (x+5, y+10), (x-5, y)])
            else:
                x, y = self.x, self.y + l
                draw.line(screen, "black", (x-20, y), (x+20, y))
                y += SEPARATION/2
                if self.is_forward:
                    draw.polygon(screen , (50, 50, 50), [(x-10, y-5), (x+10, y-5), (x, y+5)])
                else:
                    draw.polygon(screen , (50, 50, 50), [(x-10, y+5), (x+10, y+5), (x, y-5)])
            l += SEPARATION
        
        # 2. Draw inner letters
        super().draw(screen, state)

        # 3. Draw covers
        if self.is_horizontal:
            screen.blit(self.head, (self.x, self.y-40))
            screen.blit(self.tail, (self.x+self.length-80, self.y-40))
        else:
            screen.blit(self.head, (self.x-40, self.y))
            screen.blit(self.tail, (self.x-40, self.y+self.length-80))


    def update(self, state: GameState, dt: float):
        # 1. Update conveyor animation
        self._animation_tick += self.speed/SEPARATION*dt
        if (self._animation_tick >= 1):
            self._animation_tick -= 1
        
        # 2. Move Letters on the conveyor belt
        dir = 2*self.is_forward-1
        dx = self.speed*dir*dt if self.is_horizontal else 0
        dy = 0 if self.is_horizontal else self.speed*dir*dt
        for letter in self.inner_objects.sprites():
            letter.move(dx, dy)

        # 3 Remove & Add Letter to belt
        self._check_letters()
        self._time_since_new += dt
        if self._time_since_new > self.rate:
            self._time_since_new -= self.rate
            self._add_letter(state)
        
        # 4. Update Letter
        for letter in self.inner_objects.sprites():
            letter.update(state, dt)
    
    def _add_letter(self, state: GameState):
        x = (self.x if not self.is_horizontal else 
             self.x + 25 if self.is_forward else 
             self.x + self.length - 25)
        y = (self.y if self.is_horizontal else
             self.y + 25 if self.is_forward else 
             self.y + self.length - 25)
        new_letter = Letter.random(x, y, self.answer_list)
        self.inner_objects.add(new_letter)
        state.letters.add(new_letter)


    def _check_letters(self):
        letters: list[Letter] = self.inner_objects.sprites()

        if len(letters) == 0:
            return
        
        first = letters[0]
        if (self.is_forward):
            if (self.is_horizontal):
                if (first.x > self.x + self.length - 25):
                    first.kill()
            else:
                if (first.y > self.y + self.length - 25):
                    first.kill()
        else:
            if (self.is_horizontal):
                if (first.x < self.x + 25):
                    first.kill()
            else:
                if (first.y < self.y + 25):
                    first.kill()
    
    def update_answer_list(self, event):
        question: Question = event.question
        self.answer_list = [answer.text.upper() for answer in question.answers]