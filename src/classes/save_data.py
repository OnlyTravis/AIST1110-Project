import json
from enum import Enum

class SaveData(Enum):
    SkipTutorial = "skip_tutorial"
    HighScore = "high_score"
    MostAnswered = "most_answered"

class SaveDataManager:
    @classmethod
    def init_data(cls):
        with open("./data/save_data.json", "r") as file:
            cls.data = json.load(file)

    @classmethod
    def get_value(cls, key: SaveData):
        return cls.data[key.value]

    @classmethod
    def set_value(cls, key: SaveData, value):
        cls.data[key.value] = value

    @classmethod
    def save_data(cls):
        with open("./data/save_data.json", "w") as file:
            file.write(json.dumps(cls.data)) 