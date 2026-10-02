from functools import lru_cache
from google import genai
from .config import GEMINI_API_KEY

@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to the .env file.")
    return genai.Client(api_key=GEMINI_API_KEY)


def generate_text(prompt: str, model: str) -> str:
    response = get_client().models.generate_content(model=model, contents=prompt)
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()
