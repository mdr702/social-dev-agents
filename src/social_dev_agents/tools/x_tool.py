from __future__ import annotations

import httpx

from social_dev_agents.config import SETTINGS


def lookup_x_topic(query: str) -> str:
    """Recent public posts if a bearer token exists. Always read-only."""
    query = query.strip()
    if not query:
        return "No X query provided."

    if not SETTINGS.x_bearer_token:
        return (
            f"X bearer token not set. Draft a thread on '{query}' with 4 short posts: "
            "hook, tip, example, question. No auto-posting."
        )

    headers = {"Authorization": f"Bearer {SETTINGS.x_bearer_token}"}
    params = {
        "query": f"{query} -is:retweet lang:en",
        "max_results": 10,
        "tweet.fields": "public_metrics,created_at",
    }
    try:
        with httpx.Client(timeout=20.0) as client:
            r = client.get("https://api.x.com/2/tweets/search/recent", headers=headers, params=params)
            if r.status_code == 404:
                r = client.get(
                    "https://api.twitter.com/2/tweets/search/recent",
                    headers=headers,
                    params=params,
                )
            r.raise_for_status()
            data = r.json().get("data", [])
    except Exception as exc:
        return f"X search failed ({exc}). Draft from the topic only."

    if not data:
        return f"No recent public posts found for '{query}'."
    lines = [f"- {item.get('text', '')[:180]}" for item in data[:5]]
    return "Recent public X posts (read-only):\n" + "\n".join(lines)
