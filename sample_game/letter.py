import pygame

from game_obj import GameObject

class Letter(GameObject):
    def __init__(self, chr, x, y):
        self.x = x
        self.y = y
        self.chr = chr
        font = pygame.font.Font(pygame.font.get_default_font())
        self.text = font.render(chr, True, "white")
    
    def draw(self, screen: pygame.surface.Surface):
        pygame.draw.rect(screen, "black", pygame.Rect(self.x-10, self.y-10, 30, 30))
        screen.blit(self.text, (self.x, self.y))
    
    def update(self, parent):
        return