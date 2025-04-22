import pygame

from src.classes.event import event_handler
from src.classes.images import ImageLoader
from src.scenes.title import TitleScreen
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class Game:
    def __init__(self):
        # 1. Init pygame
        pygame.init()

        # 2. Set up
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.scene = TitleScreen(self.screen, self.changeScene)
        
        # 3. Add quit listener
        event_handler.add_listener(pygame.QUIT, pygame.quit)

        # 4. Load Assets
        ImageLoader.load_images()

    def run(self):
        dt = 0
        while (True):
            for event in pygame.event.get():
                event_handler.handle_event(event)

            self.scene.draw()
            self.scene.update(dt)

            pygame.display.flip()
            dt = self.clock.tick(FPS) / 1000
    
    def changeScene(self, SceneClass):
        self.scene = SceneClass(self.screen, self.changeScene)