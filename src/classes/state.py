from enum import Enum

class Gamemode(Enum):
    SinglePlayer = 0
    LocalMultiplayer = 1
    Multiplayer = 2

class GameState():
    def __init__(self):
        self._player1_pos: tuple = (-1, -1)
        self._player2_pos: tuple = (-1, -1)
        self._gamemode: Gamemode = Gamemode.SinglePlayer
    
    @property
    def player1_pos(self):
        return self._player1_pos
    
    @player1_pos.setter
    def player1_pos(self, pos: tuple):
        self._player1_pos = pos
    
    @property
    def player2_pos(self):
        return self._player2_pos
    
    @player2_pos.setter
    def player2_pos(self, pos: tuple):
        self._player2_pos = pos
    
    @property
    def gamemode(self):
        return self._gamemode

    @gamemode.setter
    def gamemode(self, gamemode: Gamemode):
        self._gamemode = gamemode