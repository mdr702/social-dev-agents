from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")


def _flag(name: str, default: bool = False) -> bool:
    raw = os.getenv(name, str(default)).strip().lower()
    return raw in {"1", "true", "yes", "on"}


@dataclass
class Settings:
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", "").strip())
    openai_model: str = field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip())
    github_token: str = field(default_factory=lambda: os.getenv("GITHUB_TOKEN", "").strip())
    youtube_api_key: str = field(default_factory=lambda: os.getenv("YOUTUBE_API_KEY", "").strip())
    x_bearer_token: str = field(default_factory=lambda: os.getenv("X_BEARER_TOKEN", "").strip())
    instagram_access_token: str = field(default_factory=lambda: os.getenv("INSTAGRAM_ACCESS_TOKEN", "").strip())
    instagram_business_account_id: str = field(
        default_factory=lambda: os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID", "").strip()
    )
    allow_live_posts: bool = field(default_factory=lambda: _flag("ALLOW_LIVE_POSTS", False))
    family_friendly: bool = field(default_factory=lambda: _flag("FAMILY_FRIENDLY", True))
    output_dir: Path = field(default_factory=lambda: ROOT / "outputs")

    @property
    def has_llm(self) -> bool:
        return bool(
            self.openai_api_key
            or os.getenv("GROQ_API_KEY", "").strip()
            or os.getenv("GEMINI_API_KEY", "").strip()
            or os.getenv("GOOGLE_API_KEY", "").strip()
            or os.getenv("OPENROUTER_API_KEY", "").strip()
        )


SETTINGS = Settings()
SETTINGS.output_dir.mkdir(parents=True, exist_ok=True)
