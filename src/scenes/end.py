from src.classes.scene import Scene, Scenes
from src.classes.state import GameState, Gamemode
from src.classes.save_data import SaveData, SaveDataManager
from src.classes.save_data import SaveDataManager, SaveData
from src.ui_element.text_button import TextButton
from src.ui_element.text import Text

class EndingScreen(Scene):
    def __init__(self, screen, to_scene, state: GameState):
        super().__init__(screen, to_scene)
        self.state = state
        self._update_highscore()
        self._add_ui_element()
    
    def _add_ui_element(self):
        w, h = self.screen.get_size()
        self.add_element(Text(w/2, 50, "Result", font_size=50))
        self.add_element(Text(w/2, 100, f"P1 Score : {self.state.player1_score}", "#ff5252", 40))
        self.add_element(Text(w/2, 130, f"P2 Score : {self.state.player2_score}", "#7ebbfc", 40))
        self.add_element(TextButton("Return to title", w/2, h-100, on_click=self._return_to_title))
    
    def _update_highscore(self):
        highscore = SaveDataManager.get_value(SaveData.HighScore)
        highscore = max(highscore, self.state.player1_score)
        if self.state.gamemode == Gamemode.LocalMultiplayer:
            highscore = max(highscore, self.state.player2_score)
        
        if highscore != SaveDataManager.get_value(SaveData.HighScore):
            SaveDataManager.set_value(SaveData.HighScore, highscore)
            SaveDataManager.save_data()
            self.add_element(Text(50, 180, f"New Highscore! : {highscore}", font_size=40))

    def draw(self):
        self.screen.fill((150, 150, 150))
        super().draw()
    
    def update(self, dt):
        super().update(dt)

    def _return_to_title(self):
        self.exit_to(Scenes.TitleScreen)