from enum import Enum
from pygame.sprite import Group

from src.constants import QUESTION_TIMER

class Gamemode(Enum):
    SinglePlayer = 0
    LocalMultiplayer = 1
    Multiplayer = 2

class States(Enum):
    BeforeStart = 0
    Playing = 1
    Ended = 2
    Paused = 3

class GameState():
    def __init__(self):
        self.player1_pos: tuple = (-1, -1)
        self.player2_pos: tuple = (-1, -1)
        self.player1_near = None
        self.player2_near = None
        self.player1_is_holding = False
        self.player2_is_holding = False
        self.player1_score = 0
        self.player2_score = 0

        self.timer = QUESTION_TIMER
        self.letters = Group()
        self.game_state = States.BeforeStart

        self.gamemode: Gamemode = Gamemode.SinglePlayer