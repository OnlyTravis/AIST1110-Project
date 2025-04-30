import pygame

from src.classes.gpt_api import GPTAPI
from src.classes.event import event_handler
from src.classes.images import ImageLoader
from src.classes.scene import Scenes
from src.classes.save_data import SaveDataManager
from src.scenes.title import TitleScreen
from src.scenes.options import OptionScreen
from src.scenes.tutorial import TutorialScreen
from src.scenes.game import GameScreen
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class Game:
    def __init__(self):
        # 1. Init pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # 2. Add quit listener
        event_handler.add_listener(pygame.QUIT, lambda e: pygame.quit())

        # 3. Load Assets
        ImageLoader.load_images()

        # 4. Init API
        GPTAPI.init_api()
        SaveDataManager.init_data()

        self.scene = TitleScreen(self.screen, self.changeScene)

    def run(self):
        dt = 0
        while (True):
            for event in pygame.event.get():
                event_handler.handle_event(event)

            self.scene.draw()
            self.scene.update(dt)

            pygame.display.flip()
            dt = self.clock.tick(FPS) / 1000
    
    def changeScene(self, scene: Scenes, **args):
        match scene:
            case Scenes.TitleScreen:
                self.scene = TitleScreen(self.screen, self.changeScene, **args)
            case Scenes.OptionScreen:
                self.scene = OptionScreen(self.screen, self.changeScene, **args)
            case Scenes.TutorialScreen:
                self.scene = TutorialScreen(self.screen, self.changeScene, **args)
            case Scenes.GameScreen:
                self.scene = GameScreen(self.screen, self.changeScene, **args)