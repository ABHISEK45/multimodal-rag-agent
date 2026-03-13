import os
from dotenv import load_dotenv
from google import genai
from anthropic import Anthropic

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "gemini")


# Configure Claude
claude_client = Anthropic(api_key=CLAUDE_API_KEY) if CLAUDE_API_KEY else None


def generate_response(prompt: str, provider: str):

    if provider == "gemini":
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text

    elif provider == "claude":
        message = claude_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text

    elif provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
        )
        return response.choices[0].message.content

    elif provider == "ollama":
        import requests
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False,
            },
        )
        return response.json()["response"]

    else:
        raise ValueError(f"Unsupported provider: {provider}")