from __future__ import annotations

import httpx

from social_dev_agents.config import SETTINGS


def lookup_github_repo(repo: str) -> str:
    """Read public GitHub repo metadata. Never writes, stars, or opens issues."""
    repo = repo.strip().strip("/")
    if not repo or "/" not in repo:
        return "Give a repo like owner/name (example: octocat/Hello-World)."

    headers = {"Accept": "application/vnd.github+json", "User-Agent": "social-dev-agents"}
    if SETTINGS.github_token:
        headers["Authorization"] = f"Bearer {SETTINGS.github_token}"

    url = f"https://api.github.com/repos/{repo}"
    try:
        with httpx.Client(timeout=20.0) as client:
            r = client.get(url, headers=headers)
            if r.status_code == 404:
                return f"Repo {repo} was not found or is private."
            r.raise_for_status()
            data = r.json()
    except Exception as exc:
        return f"GitHub lookup failed ({exc}). Using topic-only planning instead."

    desc = data.get("description") or "No description"
    license_name = (data.get("license") or {}).get("spdx_id") or "unspecified"
    return (
        f"Repo {data.get('full_name')}: {desc}. "
        f"Stars {data.get('stargazers_count', 0)}, forks {data.get('forks_count', 0)}, "
        f"language {data.get('language') or 'n/a'}, license {license_name}, "
        f"open issues {data.get('open_issues_count', 0)}, url {data.get('html_url')}."
    )
