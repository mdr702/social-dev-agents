from __future__ import annotations

import re

BLOCKED = (
    "weapon",
    "exploit",
    "malware",
    "hack into",
    "stolen account",
    "buy followers",
    "fake engagement",
    "scrape private",
    "doxx",
)

NSFW_HINTS = (
    "nsfw",
    "explicit",
    "adult only",
)


def check_topic(text: str) -> list[str]:
    lowered = text.lower()
    hits = [word for word in BLOCKED if word in lowered]
    hits += [word for word in NSFW_HINTS if word in lowered]
    return hits


def sanitize_hashtags(tags: list[str], limit: int = 8) -> list[str]:
    clean: list[str] = []
    for tag in tags:
        token = re.sub(r"[^A-Za-z0-9_]", "", tag.lstrip("#"))
        if token and token.lower() not in {t.lower() for t in clean}:
            clean.append(token)
        if len(clean) >= limit:
            break
    return clean


def family_guard(text: str) -> str:
    """Keep copy school-safe. This is a filter, not a publisher."""
    issues = check_topic(text)
    if issues:
        return f"BLOCKED: topic tripped safety terms ({', '.join(issues)}). Pick a different subject."
    return text
