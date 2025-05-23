from dotenv import load_dotenv
from openai import AzureOpenAI
from typing import Callable
import os
from threading import Thread

from src.classes.data_classes import Question, Answer

tmp_questions = [
    Question("Name a yellow fruit", [
        Answer("Banana", 51),
        Answer("Lemon", 20),
        Answer("Mango", 13),
        Answer("Pineapple", 8),
        Answer("Pear", 6),
        Answer("Starfruit", 2)
    ]),
]

PROMPT = """
Create {n} simple questions for a game similar to Family Feud.
Each question should have 6 most popular answers and 
the answers should be mostly in 1 word.
You don't have to include the question number.
Please provide the question and answers in the following format:
<Raw Question Text>
<Answer 1> <Count>
<Answer 2> <Count>...
<Raw Question Text>
...
"""

class GPTAPI():
    _client = None
    _buffer: list[Question] = []
    on_recieve = None
    is_fetching = False

    @classmethod
    def init_api(cls):
        load_dotenv()
        AZURE_API_KEY = os.getenv("AZURE_API_KEY")

        if AZURE_API_KEY == None:
            key = input("Please Provide an api key: ")
            with open(".env", "w") as env:
                env.write(f"AZURE_API_KEY = {key}")
            AZURE_API_KEY = key

        cls._client = AzureOpenAI(
            azure_endpoint="https://cuhk-apip.azure-api.net",
            api_version="2024-02-01",  # Use appropriate version for your model
            api_key=AZURE_API_KEY
        )
        cls._fetch_questions()
    
    @classmethod
    def _fetch_questions(cls):
        """
        An internal function for fetching questions 
        from the api into the buffer.
        """
        if cls.is_fetching:
            return

        cls.is_fetching = True
        def fetch():
            # 1. Calling API
            response = cls._client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": PROMPT.format(n=5)}
                ],
                temperature=0.7,
            )

            # 2. Processing Texts & Appending questions to buffer
            full_text = response.choices[0].message.content
            lines: list[str] = []
            i = 0
            for line in full_text.splitlines():
                if line.strip() == "":
                    continue
                
                lines.append(line)
                i += 1

                if i == 7:
                    answers = []
                    for line_ in lines[1:7]:
                        split = line_.strip().split(" ")
                        num = int(split[-1])
                        answer = "".join(split[0 : len(split)-1]).replace(" ", "")
                        answers.append(Answer(answer, num))

                    cls._buffer.append(Question(
                        lines[0],
                        answers
                    ))
                    i = 0
                    lines = []

            cls.is_fetching = True
            if cls.on_recieve != None:
                cls.on_recieve(cls._buffer.pop())
                cls.on_recieve = None
        Thread(target=fetch).start()

    """
    # An overwrite for the function _fetch_questions to avoid wasting api calls in testing
    @classmethod
    def _fetch_questions(cls):
        cls._buffer = tmp_questions*6
    """

    @classmethod
    def get_question(cls, on_recieve: Callable[[Question], None]) -> None:
        """
        Pops question from buffer.
        If the length of buffer is less than 2 after popping,
        Fetches 5 questions from the gpt-4o in a separate thread
        """
        if len(cls._buffer) <= 2:
            cls._fetch_questions()

        if len(cls._buffer) == 0:
            cls.on_recieve = on_recieve
            return

        on_recieve(cls._buffer.pop())
