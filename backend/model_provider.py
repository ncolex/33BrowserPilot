import os
import google.generativeai as genai


DEFAULT_MODEL_CANDIDATES = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]


def get_gemini_model():
    """Return a configured Gemini model with robust defaults.

    Prioritizes `GEMINI_MODEL` from environment and falls back to stable public models.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is missing. Configure it in your environment to enable LLM calls."
        )

    genai.configure(api_key=api_key)

    configured_model = os.getenv("GEMINI_MODEL", "").strip()
    model_name = configured_model or DEFAULT_MODEL_CANDIDATES[0]

    return genai.GenerativeModel(model_name)

