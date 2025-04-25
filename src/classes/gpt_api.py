from dotenv import load_dotenv
from openai import AzureOpenAI
import os

from src.classes.data_classes import Question, Answer

load_dotenv()
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
'''
# Initialize the client
client = AzureOpenAI(
    azure_endpoint="https://cuhk-apip.azure-api.net",
    api_version="2024-02-01",  # Use appropriate version for your model
    api_key=AZURE_API_KEY
)

# Chat with gpt-4o-mini or gpt-4o
response = client.chat.completions.create(
    model="gpt-4o",  # or "gpt-4o"
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": (
            "Create 3 questions, "
            "each with 10 most popular answers, "
            "for playing the 'Guess Their Answer' game."
        )}
    ],
    temperature=0.7,  # Control response creativity (0-1)
)
print(response.choices[0].message.content)
'''

tmp_questions = [
    Question("Name a yellow fruit", [
        Answer("Banana", 51),
        Answer("Lemon", 20),
        Answer("Manga", 13),
        Answer("Pineapple", 8),
        Answer("Pear", 6),
        Answer("Starfruit", 2)
    ]),
    Question("Name a asdsad fruit", [
        Answer("asg", 51),
        Answer("Legdsgmon", 20),
        Answer("gs", 13),
        Answer("Pidsdsfneapple", 8),
        Answer("asdfsa", 6),
        Answer("vcx", 2)
    ]),
    Question("Name a aaaa fruit", [
        Answer("aaa", 51),
        Answer("Levvvmoan", 20),
        Answer("vv", 13),
        Answer("vvaa", 8),
        Answer("aasasd", 6),
        Answer("rtrtr", 2)
    ]),
]

prompt = """
Create 3 simple questions for a game similar to Family Feud.
Each question should have 6 most popular answers and 
the answers should be mostly in 1 word.
You don't have to provide the numbers.
Please provide the question and answers in the following format:
1. <Question Text>
<Answer 1>
<Answer 2>...
2. <Question Text>
...
"""

# Things commented out to prevent wasting of api calls during coding / testing
class GPTAPI():
    _client = None
    tmp_i = 0

    @classmethod
    def init_api(cls):
        cls._client = AzureOpenAI(
            azure_endpoint="https://cuhk-apip.azure-api.net",
            api_version="2024-02-01",  # Use appropriate version for your model
            api_key=AZURE_API_KEY
        )

    @classmethod
    def get_question(cls) -> Question:
        # todo implement api calls
        response = cls._client.chat.completions.create(
            model="gpt-4o",  # or "gpt-4o"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,  # Control response creativity (0-1)
        )
        tr
        print(response)
        cls.tmp_i += 1
        return tmp_questions[cls.tmp_i-1]