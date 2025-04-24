class Answer:
    def __init__(self, answer: str, score: int):
        self.answer = answer
        self.score = score

class Question:
    def __init__(self, text: str, answers: list[Answer]):
        self.text = text
        self.answers = answers