from __future__ import annotations

import os
from dataclasses import dataclass

import httpx

from social_dev_agents.config import SETTINGS


@dataclass
class LLMTarget:
    name: str
    base_url: str
    api_key: str
    model: str


def resolve_llm() -> LLMTarget | None:
    """Pick a free or cheap OpenAI-compatible endpoint.

    Order: Groq (free, no card) → Gemini OpenAI-compat → OpenRouter free → OpenAI.
    """
    groq = os.getenv("GROQ_API_KEY", "").strip()
    if groq:
        return LLMTarget(
            name="groq",
            base_url="https://api.groq.com/openai/v1",
            api_key=groq,
            model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
        )

    gemini = os.getenv("GEMINI_API_KEY", "").strip() or os.getenv("GOOGLE_API_KEY", "").strip()
    if gemini:
        return LLMTarget(
            name="gemini",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai",
            api_key=gemini,
            model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        )

    openrouter = os.getenv("OPENROUTER_API_KEY", "").strip()
    if openrouter:
        return LLMTarget(
            name="openrouter",
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter,
            model=os.getenv("OPENROUTER_MODEL", "openrouter/auto"),
        )

    if SETTINGS.openai_api_key:
        return LLMTarget(
            name="openai",
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            api_key=SETTINGS.openai_api_key,
            model=SETTINGS.openai_model,
        )
    return None


def chat(prompt: str, system: str = "You write short, school-safe drafts. No posting.") -> str:
    target = resolve_llm()
    if target is None:
        return (
            "No free AI token found. Create one (no credit card) at "
            "https://console.groq.com/keys or https://aistudio.google.com/apikey "
            "then set GROQ_API_KEY or GEMINI_API_KEY in .env"
        )

    headers = {
        "Authorization": f"Bearer {target.api_key}",
        "Content-Type": "application/json",
    }
    if target.name == "openrouter":
        headers["HTTP-Referer"] = "https://github.com/mdr702/social-dev-agents"
        headers["X-Title"] = "social-dev-agents"

    payload = {
        "model": target.model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.4,
    }
    url = target.base_url.rstrip("/") + "/chat/completions"
    try:
        with httpx.Client(timeout=45.0) as client:
            r = client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
        return data["choices"][0]["message"]["content"]
    except Exception as exc:
        return f"{target.name} call failed ({exc}). Check the key and model id."
