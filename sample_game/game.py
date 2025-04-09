import pygame
import string
import random

from player import Player
from game_obj import GameObject
from letter import Letter

class Game:
    def __init__(self):
        pygame.init()
    
    def add_letter(self, screen_size):
        chr = random.choice(string.ascii_uppercase)
        x = random.random()*screen_size[0]
        y = random.random()*screen_size[1]
        self.objects.append(Letter(chr, x, y))
    
    def run(self):
        self.objects: list[GameObject] = []
        self.objects.append(Player())

        screen = pygame.display.set_mode((1280, 720))
        clock = pygame.time.Clock()
        running = True
        dt = 0

        for i in range(10):
            self.add_letter(screen.get_size())

        while running:
            self.update()
            self.draw(screen)

            pygame.display.flip()

            dt = clock.tick(60) / 1000

        pygame.quit()


    def draw(self, screen):
        screen.fill("white")
        for obj in self.objects:
            obj.draw(screen)
    
    def update(self):
        for obj in self.objects:
            obj.update(self)
