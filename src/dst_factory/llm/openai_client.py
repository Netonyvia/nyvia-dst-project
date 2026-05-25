from openai import OpenAI

from dst_factory.config import get_settings

class OpenAIClient:

    def __init__(self, client:OpenAI | None = None) -> None:
        self.settings = get_settings()
        self.client = client or OpenAI(api_key=self.settings.openai_api_key)


    def generate_text(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.settings.openai_model,
            input=prompt
            )
        
        return response.text
    
    


    