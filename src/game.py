import pygame

from src.games.event import event_handler
from src.options import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        event_handler.addListener(pygame.QUIT, pygame.quit)
    
    def run(self):
        while (True):
            for event in pygame.event.get():
                event_handler.handle_event(event)

            self.clock.tick(FPS)