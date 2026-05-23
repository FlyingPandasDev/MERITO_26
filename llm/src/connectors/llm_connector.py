import os
from pathlib import Path

import requests
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(ENV_PATH)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")


def _get_headers():
    if not OPENROUTER_API_KEY:
        raise ValueError("Missing OPENROUTER_API_KEY in environment variables.")

    return {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }


def _get_model():
    if not OPENROUTER_MODEL:
        raise ValueError("Missing OPENROUTER_MODEL in environment variables.")

    return OPENROUTER_MODEL


def _chat_completion(messages, max_tokens):
    response = requests.post(
        f"{OPENROUTER_BASE_URL}/chat/completions",
        headers=_get_headers(),
        json={
            "model": _get_model(),
            "messages": messages,
            "temperature": 0,
            "top_p": 0.1,
            "max_tokens": max_tokens,
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    try:
        content = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as e:
        raise ValueError("Invalid OpenRouter response structure: missing choices[0].message.content") from e

    if not isinstance(content, str):
        raise ValueError("Invalid OpenRouter response structure: content is not a string")

    return content.strip()

def handshake():
    try:
        model_status = _chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": "Respond only with: True",
                },
                {
                    "role": "user",
                    "content": "If you can read this, return only: True",
                },
            ],
            max_tokens=5,
        )
        print(f"Model status: {model_status}")

    except Exception as e:
        print(f"Handshake failed: {e}")
        model_status = False

    return model_status


def use_chat(msg):
    try:
        llm_response = _chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": "Answer only the user's message. Do not repeat the prompt. Do not explain your instructions.",
                },
                {
                    "role": "user",
                    "content": msg,
                },
            ],
            max_tokens=256,
        )

    except Exception as e:
        print(f"LLM call failed: {e}")
        llm_response = None

    return llm_response
