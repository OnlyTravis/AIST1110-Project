from pygame import draw, Rect
from pygame.surface import Surface
from pygame.sprite import Group

from src.classes.state import GameState
from src.classes.data_classes import Question
from src.classes.event import GameEvent
from src.classes.ui_element import UIElement
from src.ui_element.text import Text, TextAlign

class QuestionBox(UIElement):
    def __init__(self, x, y):
        super().__init__(x, y, recursive=True)
        self.w = 800
        self.h = 200
        self.question_height = 70
        self.padding = 5

        self.question: Question = None
        self.question_visible = False
        self.revealed = [False] * 6

        self.count_down: float = 4

        self._set_up_ui()
        self.add_event_listener(GameEvent.GameStart, self._on_start_game)
        self.add_event_listener(GameEvent.UpdateQuestion, self._on_update_question)
        self.add_event_listener(GameEvent.SubmitStatus, self._on_submit)

    def draw(self, screen: Surface):
        draw.rect(screen, "yellow", (self.x-self.w/2, self.y-self.h/2, self.w, self.h))
        draw.rect(screen, "black", (self.x-self.w/2, self.y-self.h/2, self.w, self.question_height))
        for rect in self.rects:
            draw.rect(screen, "black", rect)

        for answer in self.answers.sprites():
            answer.draw(screen)
        super().draw(screen)
    
    def update(self, dt: float):
        if self.count_down >= dt:
            self.count_down -= dt
            if int(self.count_down) < int(self.count_down + dt):
                if int(self.count_down) == 0:
                    self._set_question_text("Start!")
                else:
                    self._set_question_text(str(int(self.count_down)))

    def reveal_answer(self, index):
        if self.revealed[index]:
            return
        
        self.revealed[index] = True
        answer_text: Text = self.answers.sprites()[index]
        answer_text.set_text(f"{index+1}. {self.question.answers[index].text}")

    def _set_up_ui(self):
        self.add_inner_element(Text(self.x, self.y-self.h/2+self.question_height/2, "3", "white", 40))
        self.rects: list[Rect] = []
        self.answers = Group()
        w = (self.w - 3*self.padding)/2
        h = (self.h - self.question_height - 4*self.padding)/3
        for i in range(6):
            x = i%2
            y = int(i/2)
            rect = Rect(
                self.x - self.w/2 + self.padding + (w+self.padding)*x,
                self.y - self.h/2 + self.question_height + self.padding + (h+self.padding)*y,
                w,
                h
            )
            self.rects.append(rect)
            self.answers.add(Text(
                x=rect.x, 
                y=rect.y+h/2,
                text=f"{i+1}. ", 
                color="white",
                align=TextAlign.Start
            ))

    def _set_question_text(self, text):
        self.inner_elements.sprites()[0].set_text(text)

    def _on_start_game(self, event):
        self.question_visible = True
        self.count_down = -1

        if self.question != None:
            self._set_question_text(self.question.text)

    def _on_update_question(self, event):
        self.question = event.question
        if self.question_visible:
            self._set_question_text(event.question.text)

    def _on_submit(self, event):
        if not event.is_correct:
            return
    
        self.reveal_answer(event.answer_index)
    
    def kill(self):
        for answer in self.answers.sprites():
            answer.kill()
        super().kill()
