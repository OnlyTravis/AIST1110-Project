from src.classes.event import GameEvent, EventListener
from src.classes.state import GameState, States
from src.classes.gpt_api import GPTAPI
from src.classes.data_classes import Question
from src.constants import QUESTION_TIMER, QUESTION_PER_GAME

class GameManager(EventListener):
    def __init__(self, state: GameState):
        super().__init__()
        self.state = state
        self.timer = QUESTION_TIMER
        self.reveal_timer = -1

        self.waiting_question = False
        self.question = None
        self.question_num = 0
        self.answered = [False] * 6

        GameEvent.GameStart.set_timeout(4000)
        GPTAPI.get_question(self._on_recieve_question)
        self.add_event_listener(GameEvent.SubmitWord, self._on_submit)
    
    def _on_recieve_question(self, question: Question):
        self.question = question
        GameEvent.UpdateQuestion.post({"question": question})

    def update(self, state: GameState, dt: float):
        # 1. Handle Question Timers
        self._handle_timer(state, dt)
        
    def _handle_timer(self, state: GameState, dt: float):
        # 1. Return if not playing
        if state.game_state != States.Playing:
            return
        
        if self.reveal_timer == -1:
            # 2. Update timer & state.timer
            self.timer -= dt
            if self.timer > 0:
                state.timer = self.timer
                return
            
            # 3. Reveal Answer & set reveal timer
            GameEvent.post(GameEvent.RevealAnswers)
            self.reveal_timer = 3

        # 4. Reveal Timer
        self.reveal_timer -= dt
        if self.reveal_timer > 0:
            return
        
        self.reveal_timer = -1
        if self.question_num + 1 == QUESTION_PER_GAME:
            # End Game
            self.timer = 0
            state.timer = self.timer
            GameEvent.post(GameEvent.GameEnd)
            return
        
        # Next Question (reset timer)
        self.question_num += 1
        self.answered = [False] * 6
        self.timer = QUESTION_TIMER
        state.timer = self.timer
        GPTAPI.get_question(self._on_recieve_question)
 
    def _on_submit(self, event):
        # 1. Check Word
        index = -1
        for i, answer in enumerate(self.question.answers):
            if answer.text.lower() == event.word.lower():
                index = i
                break

        # 2. Update Score
        is_correct = (index != -1) and not self.answered[index]
        if is_correct:
            self.answered[index] = True
            score = self.question.answers[index].score + len(self.question.answers[index].text)
            if event.is_p1:
                self.state.player1_score += score
            else:
                self.state.player2_score += score

        # 3. Boardcast Event
        GameEvent.SubmitStatus.post({
            "is_p1": event.is_p1,
            "is_correct": is_correct,
            "answer_index": index,
            "p1_score": self.state.player1_score,
            "p2_score": self.state.player2_score
        })
    
    def __del__(self):
        self.remove_all_listeners()