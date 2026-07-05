import os

import requests

FEATHERLESS_URL = "https://api.featherless.ai/v1/chat/completions"
DEFAULT_MODEL = os.environ.get("FEATHERLESS_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")

SYSTEM_PROMPT = (
    "You are the health assistant inside Sanjeevani, a self care and health "
    "literacy application with the theme Be Your Own Doctor. Answer health "
    "questions in plain, direct language. Keep replies short and practical. "
    "Always remind the user that this is general information, not a diagnosis, "
    "and that a licensed doctor should be consulted for anything serious or "
    "urgent. Do not use emojis. Do not use em dashes."
)


def ask_assistant(message, history=None):
    api_key = os.environ.get("FEATHERLESS_API_KEY")
    if not api_key:
        return {
            "ok": False,
            "reply": "The assistant is not configured yet. Add a Featherless AI API key to enable this feature.",
        }

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history[-10:])
    messages.append({"role": "user", "content": message})

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "*",
        "X-Title": "Sanjeevani",
    }
    payload = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "max_tokens": 400,
        "temperature": 0.4,
    }

    try:
        response = requests.post(FEATHERLESS_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"].strip()
        return {"ok": True, "reply": reply}
    except requests.exceptions.RequestException as exc:
        return {
            "ok": False,
            "reply": "The assistant could not be reached right now. Please try again in a moment.",
            "error": str(exc),
        }
    except (KeyError, IndexError):
        return {
            "ok": False,
            "reply": "The assistant returned an unexpected response. Please try again.",
        }
