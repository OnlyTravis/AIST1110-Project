from collections.abc import Callable
from pygame import KEYDOWN, K_SPACE, event, surface
from pygame.sprite import Group

from src.classes.images import ImageLoader, Images
from src.classes.scene import Scene
from src.classes.save_data import SaveData, SaveDataManager
from src.classes.scene import Scenes
from src.ui_element.text import Text, TextAlign
from src.ui_element.text_button import TextButton

class TutorialScreen(Scene):
    def __init__(self, screen: surface.Surface, to_scene: Callable, **args):
        super().__init__(screen, to_scene)
        self.other_args = args  # Passes to GameScreen

        self.page = 0
        self.images_1 = ImageLoader.get_frames(Images.Tutorial1, 300, 150, 150)
        self.images_2 = ImageLoader.get_frames(Images.Tutorial2, 600, 450, 150)
        self._init_ui()

        self.page_ele = Group()
        self.load_page()

    def _init_ui(self):
        w, h = self.screen.get_size()
        self.add_element(Text(w/2, 50, "Tutorial", font_size=50))
    
    def load_page(self):
        w, h = self.screen.get_size()

        for ele in self.page_ele.sprites():
            ele.kill()

        if self.page == 0:
            self.page_ele.add(Text(50, 100, "P1 controls: ", "#ff5252", align=TextAlign.Start))
            self.page_ele.add(Text(50, 130, "Movement : WASD", "#ff5252", align=TextAlign.Start))
            self.page_ele.add(Text(50, 160, "Interact : E", "#ff5252", align=TextAlign.Start))
            self.page_ele.add(Text(400, 100, "P2 controls: ", "#7ebbfc", align=TextAlign.Start))
            self.page_ele.add(Text(400, 130, "Movement : Arrow Keys", "#7ebbfc", align=TextAlign.Start))
            self.page_ele.add(Text(400, 160, "Interact : Enter Key", "#7ebbfc", align=TextAlign.Start))
            self.page_ele.add(Text(50, 240, "Players can pick up / swap holding letters", align=TextAlign.Start))
            self.page_ele.add(Text(50, 270, "on the conveyor belt", align=TextAlign.Start))
            self.page_ele.add(TextButton("Next Page", w/2, h-80, self.next_page))
        else:
            self.page_ele.add(Text(50, 100, "Players will need to guess the most popular answer", align=TextAlign.Start))
            self.page_ele.add(Text(50, 130, "to the question by assembling the correct word.", align=TextAlign.Start))
            self.page_ele.add(Text(50, 170, "If the answer is in two words, the spaces can be ignored.", align=TextAlign.Start))
            self.page_ele.add(Text(50, 200, "(e.g. apple pie -> applepie)", align=TextAlign.Start))
            self.page_ele.add(Text(50, 480, "Players can then submit their answer by", align=TextAlign.Start))
            self.page_ele.add(Text(50, 510, "interacting with the submit button", align=TextAlign.Start))
            self.page_ele.add(Text(50, 550, "Bonus point will be awarded ", align=TextAlign.Start))
            self.page_ele.add(Text(50, 580, "based on length of answer", align=TextAlign.Start))
            self.page_ele.add(TextButton("Previouse Page", w/2 - 200, h-80, self.previous_page))
            self.page_ele.add(TextButton("Start Game", w/2 + 200, h-80, self.start_game))


    def draw(self):
        w, h = self.screen.get_size()
        self.screen.fill((200, 200, 200))
        
        for ele in self.page_ele.sprites():
            ele.draw(self.screen)

        if self.page == 0:
            self.screen.blit(self.images_1[0], (800, 180))
            self.screen.blit(self.images_1[1], (960, 180))
            self.screen.blit(self.images_1[2], (800, 340))
            self.screen.blit(self.images_1[3], (960, 340))
        else:
            self.screen.blit(self.images_2[0], (w/2-525, 240))
            self.screen.blit(self.images_2[1], (w/2+75, 240))
            self.screen.blit(self.images_2[2], (w-500, 460))

        super().draw()

    def update(self, dt):
        self.page_ele.update(dt=dt)
        super().update(dt)
    
    def exit(self):
        for ele in self.page_ele.sprites():
            ele.kill()
        super().exit()

    def previous_page(self):
        self.page -= 1
        self.load_page()

    def next_page(self): 
        self.page += 1
        self.load_page()
    
    def start_game(self):
        SaveDataManager.set_value(SaveData.SkipTutorial, True)
        SaveDataManager.save_data()
        self.exit_to(Scenes.GameScreen, **self.other_args)