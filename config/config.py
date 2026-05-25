from pydantic_settings import BaseSettings


class Config(BaseSettings):
    OPENAI_API_KEY: str
    mock_response: bool = False
    model_name: str = "openai/gpt-5-nano"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # extra = "allow"


config = Config()
