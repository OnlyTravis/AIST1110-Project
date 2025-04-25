class Answer:
    def __init__(self, text: str, score: int):
        self.text = text
        self.score = score

class Question:
    def __init__(self, text: str, answers: list[Answer]):
        self.text = text
        self.answers = answers