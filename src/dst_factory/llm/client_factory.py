from typing import Protocol

from dst_factory.config import get_settings
from dst_factory.llm.gemini_client import GeminiClient
from dst_factory.llm.openai_client import OpenAIClient


class TextGenerationClient(Protocol):
    def generate_text(self, prompt: str) -> str:
        ...


def build_llm_client() -> TextGenerationClient:
    settings = get_settings()

    if settings.llm_provider == "gemini":
        return GeminiClient()

    if settings.llm_provider == "openai":
        return OpenAIClient()

    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")

