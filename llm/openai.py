from openai import OpenAI

class OpenAILLM:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content