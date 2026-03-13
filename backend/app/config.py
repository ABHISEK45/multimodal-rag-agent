import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

settings = Settings()