from google import genai

from dst_factory.config import get_settings


class GeminiClient:

    def __init__(self):
        self.settings = get_settings()
        
        if not self.settings.gemini_api_key:
            raise ValueError("Gemini API key is not set in the environment variables.")
        

        self.client = genai.Client(api_key=self.settings.gemini_api_key)

    def generate_text(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt
        )
        return response.text or ""
    


