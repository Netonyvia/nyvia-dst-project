from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.5"


    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"

    llm_provider: str = "gemini"

    google_client_secret_file: str = "credentials.json"
    google_token_file: str = "token.json"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def get_settings() -> Settings:
    return Settings()

