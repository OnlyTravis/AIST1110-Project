import pygame

from src.games.event import event_handler
from src.games.scene import Scene
from src.scenes.title import TitleScreen
from src.options import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class Game:
    def __init__(self):
        # 1. Init pygame
        pygame.init()

        # 2. Set up
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.scene = TitleScreen(self.screen, self.changeScene)
        
        # 3. Add quit listener
        event_handler.addListener(pygame.QUIT, pygame.quit)

    def run(self):
        while (True):
            for event in pygame.event.get():
                event_handler.handle_event(event)

            self.scene.draw()
            self.scene.update()

            pygame.display.flip()
            self.clock.tick(FPS)
    
    def changeScene(self, SceneClass):
        self.scene = SceneClass(self.screen, self.changeScene)