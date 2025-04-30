from pygame import draw, Rect
from pygame.surface import Surface
from pygame.sprite import Group

from src.classes.images import ImageLoader, Images
from src.classes.data_classes import Question
from src.classes.event import GameEvent
from src.classes.ui_element import UIElement
from src.ui_element.text import Text, TextAlign

class QuestionBox(UIElement):
    def __init__(self, x, y):
        super().__init__(x, y, recursive=True)
        self.w = 800
        self.h = 195
        self.question_height = 80
        self.padding = 15
        
        self.img = ImageLoader.get(Images.QuestionBox, self.w, self.h)

        self.question: Question = None
        self.question_visible = False
        self.revealed = [False] * 6

        self.count_down: float = 4

        self._set_up_ui()
        self.add_event_listener(GameEvent.GameStart, self._on_start_game)
        self.add_event_listener(GameEvent.UpdateQuestion, self._on_update_question)
        self.add_event_listener(GameEvent.SubmitStatus, self._on_submit)
        self.add_event_listener(GameEvent.RevealAnswers, self._on_reveal_all)

    def draw(self, screen: Surface):
        screen.blit(self.img, (self.x-self.w/2, self.y-self.h/2))

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
    
    def hide_answer(self, index):
        if not self.revealed[index]:
            return

        self.revealed[index] = False
        answer_text: Text = self.answers.sprites()[index]
        answer_text.set_text(f"{index+1}. ")

    def _set_up_ui(self):
        self.add_inner_element(Text(self.x, self.y-self.h/2+self.question_height/2, "3", "black", 25))
        self.answers = Group()
        w = (self.w - 3*self.padding)/2
        h = (self.h - self.question_height - 4*self.padding)/3
        for i in range(6):
            x = i%2
            y = int(i/2)
            self.answers.add(Text(
                x=self.x - self.w/2 + self.padding + (w+self.padding)*x+8, 
                y=self.y - self.h/2 + self.question_height + self.padding + (h+self.padding)*y,
                text=f"{i+1}. ", 
                color="black",
                font_size=25,
                align=TextAlign.Start
            ))

    def _set_question_text(self, text):
        self.inner_elements.sprites()[0].set_text(text)

    def _on_start_game(self, event):
        self.question_visible = True
        self.count_down = -1

        if self.question == None:
            self._set_question_text("Waiting For Question...")
        else:
            self._set_question_text(self.question.text)

    def _on_reveal_all(self, event):
        for i in range(6):
            self.reveal_answer(i)

    def _on_update_question(self, event):
        # 1. Hide all answers
        for i in range(6):
            self.hide_answer(i)

        # 2. Update Question display
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
