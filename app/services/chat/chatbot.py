import os
import openai
from dotenv import load_dotenv
from .chatbot_schema import affirmation_response

load_dotenv()

class Chatbot:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def chat_with_AI(self, input_data: dict) -> affirmation_response:
        prompt = self.create_prompt(input_data)
        response = self.get_openai_response(prompt)
        return affirmation_response(affirmation=response)

    def create_prompt(self,input_data: dict):
        return f"""demo"""


    def get_openai_response(self, prompt: str) -> str:
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        return completion.choices[0].message.content.strip()
