from __future__ import annotations

import httpx

from social_dev_agents.config import SETTINGS


def lookup_youtube(query: str) -> str:
    """Search public YouTube videos if an API key exists. Otherwise return a planning hint."""
    query = query.strip()
    if not query:
        return "No YouTube query provided."

    if not SETTINGS.youtube_api_key:
        return (
            f"YouTube API key not set. Plan a short, helpful video on '{query}': "
            "hook in 5 seconds, 3 chapters, end screen with one next-step link. "
            "Do not auto-upload."
        )

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 5,
        "safeSearch": "strict",
        "key": SETTINGS.youtube_api_key,
    }
    try:
        with httpx.Client(timeout=20.0) as client:
            r = client.get("https://www.googleapis.com/youtube/v3/search", params=params)
            r.raise_for_status()
            items = r.json().get("items", [])
    except Exception as exc:
        return f"YouTube search failed ({exc}). Plan from the topic only."

    if not items:
        return f"No public videos found for '{query}'."

    lines = []
    for item in items:
        sn = item.get("snippet", {})
        vid = item.get("id", {}).get("videoId", "")
        lines.append(f"- {sn.get('title')} (https://youtu.be/{vid}) by {sn.get('channelTitle')}")
    return "Public YouTube references (safeSearch=strict):\n" + "\n".join(lines)
