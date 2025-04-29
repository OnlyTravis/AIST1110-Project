from pygame.sprite import Group

from src.classes.scene import Scene
from src.classes.state import Gamemode
from src.classes.images import Images
from src.classes.scene import Scenes
from src.ui_element.text_button import TextButton
from src.ui_element.text import Text
from src.ui_element.image import Image

class OptionScreen(Scene):
    def __init__(self, screen, to_scene):
        super().__init__(screen, to_scene)

        self._add_ui_element()
        self._set_gamemode(Gamemode.SinglePlayer)
    
    def _add_ui_element(self):
        w, h = self.screen.get_size()

        self.add_element(Image(w/2, h/2, w, h, Images.Background1))
        self.add_element(Text(w/2, 50, "Select Gamemode", font_size=50))
        self.add_element(Text(150, 150, "Gamemode : "))
        self.add_element(TextButton("Start Game", w/2, h-50, on_click=self._on_start_game, border_radius=10))

        self.gamemode_buttons = Group()
        self.gamemode_buttons.add(TextButton("SinglePlayer", 400, 150, on_click=lambda: self._set_gamemode(Gamemode.SinglePlayer), border_radius=10))
        self.gamemode_buttons.add(TextButton("Local Multiplayer", 700, 150, on_click=lambda: self._set_gamemode(Gamemode.LocalMultiplayer), border_radius=10))
        self.gamemode_buttons.add(TextButton("Multiplayer", 1000, 150, on_click=lambda: self._set_gamemode(Gamemode.Multiplayer), border_radius=10))
    
    def draw(self):
        super().draw()
        for button in self.gamemode_buttons.sprites():
            button.draw(self.screen)
    
    def update(self, dt):
        super().update(dt)
        self.gamemode_buttons.update(dt)

    def _set_gamemode(self, gamemode: Gamemode):
        self.selected_gamemode = gamemode
        for button in self.gamemode_buttons.sprites():
            button.text.set_color("black")

        i = 0
        if gamemode == Gamemode.LocalMultiplayer:
            i = 1
        elif gamemode == Gamemode.Multiplayer:
            i = 2
        button: TextButton = self.gamemode_buttons.sprites()[i]
        button.text.set_color("red")

    def _on_start_game(self):
        self.exit_to(Scenes.TutorialScreen, gamemode=self.selected_gamemode)