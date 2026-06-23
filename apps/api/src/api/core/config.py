from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    OPENAI_API_KEY: str
    GOOGLE_API_KEY: str
    DEEPSEEK_API_KEY: str
    DEEPSEEK_BASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")


config = Config()