from src.classes.event import GameEvent
from src.classes.state import GameState, States
from src.classes.gpt_api import GPTAPI
from src.constants import QUESTION_TIMER, QUESTION_PER_GAME

class GameManager:
    def __init__(self):
        self.timer = QUESTION_TIMER

        self.waiting_question = False
        self.question = None
        self.question_num = 0
        self.question_buffer = None

        self._fetch_question()
        GameEvent.set_timeout(GameEvent.GameStart, 4000)
        

    def update(self, state: GameState, dt: float):
        # 1. Handle Question Timers
        self._handler_timer(state, dt)

        # 2. Fetch Question if needed
        if (not self.waiting_question and 
            self.question_buffer == None and
            self.question_num + 1 != QUESTION_PER_GAME):
            self._fetch_question()
        
    def _handler_timer(self, state: GameState, dt: float):
        if state.game_state != States.Playing:
            return
        
        self.timer -= dt
        if self.timer > 0:
            state.timer = self.timer
            return
        
        if self.question_num + 1 == QUESTION_PER_GAME:
            # End Game
            self.timer = 0
            state.timer = self.timer
            GameEvent.post(GameEvent.GameEnd)
            return
        
        # Next Question (reset timer)
        self.question_num += 1
        self.timer = QUESTION_TIMER
        state.timer = self.timer
        self.question = self.question_buffer

    def _fetch_question(self):
        self.waiting_question = True

        # multithread later
        question = GPTAPI.get_question()
        if self.question == None:
            self.question = question
            GameEvent.post(GameEvent.UpdateQuestion, {"question": question})
        else:
            self.question_buffer = question

        self.waiting_question = False