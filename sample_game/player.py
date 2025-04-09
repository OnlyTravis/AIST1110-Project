import pygame
import pygame.draw

from game_obj import GameObject
from letter import Letter

class Player(GameObject):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 5
        self.holding = -1
    
    def draw(self, screen: pygame.surface.Surface):
        w, h = screen.get_size()
        pygame.draw.circle(screen, "red", (self.x, self.y), 15)
        if (self.holding != -1):
            self.holding.x = self.x
            self.holding.y = self.y
            self.holding.draw(screen)
    
    def update(self, parent):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    for obj in parent.objects:
                        if (not isinstance(obj, Letter)):
                            continue

                        if (self.check_letter(parent, obj)):
                            break
                    else:
                        if self.holding != -1:
                            self.drop_current_letter(parent)
                if event.key == pygame.K_g:
                    parent.add_letter((1280, 720))
    
    def check_letter(self, parent, letter: Letter) -> bool:
        if (self.check_is_near(letter)):
            if (self.holding != -1):
                self.drop_current_letter(parent)

            self.holding = letter
            parent.objects.remove(letter)
            return True
        return False
            

    def drop_current_letter(self, parent):
        parent.objects.append(self.holding)
        self.holding = -1

    def check_is_near(self, letter: Letter) -> bool:
        dist = abs(self.x - letter.x) + abs(self.y - letter.y)
        if (dist < 30):
            return True
        return False
                    
                