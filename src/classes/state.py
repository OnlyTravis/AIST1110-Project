from enum import Enum

class Gamemode(Enum):
    SinglePlayer = 0
    LocalMultiplayer = 1
    Multiplayer = 2

class GameState():
    def __init__(self):
        self._p1_pos: tuple = (-1, -1)
        self._p2_pos: tuple = (-1, -1)
        self._p1_near = None
        self._p2_near = None
        self._p1_is_holding = False
        self._p2_is_holding = False
        self._gamemode: Gamemode = Gamemode.SinglePlayer
    
    @property
    def player1_pos(self):
        return self._p1_pos
    
    @player1_pos.setter
    def player1_pos(self, pos: tuple):
        self._p1_pos = pos
    
    @property
    def player2_pos(self):
        return self._p2_pos
    
    @player2_pos.setter
    def player2_pos(self, pos: tuple):
        self._p2_pos = pos
    
    @property
    def player1_near(self):
        return self._p1_near
    
    @player1_near.setter
    def player1_near(self, obj):
        self._p1_near = obj
    
    @property
    def player2_near(self):
        return self._p2_near
    
    @player2_near.setter
    def player2_near(self, obj):
        self._p2_near = obj

    @property
    def player1_is_holding(self):
        return self._p1_is_holding
    
    @player1_is_holding.setter
    def player1_is_holding(self, value: bool):
        self._p1_is_holding = value
    
    @property
    def player2_is_holding(self):
        return self._p2_is_holding

    @player2_is_holding.setter
    def player2_is_holding(self, value: bool):
        self._p2_is_holding = value
    
    @property
    def gamemode(self):
        return self._gamemode

    @gamemode.setter
    def gamemode(self, gamemode: Gamemode):
        self._gamemode = gamemode