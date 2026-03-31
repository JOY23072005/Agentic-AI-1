import google.generativeai as genai

class GeminiLLM:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

    def generate(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text.strip()