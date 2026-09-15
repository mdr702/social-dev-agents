from __future__ import annotations

from social_dev_agents.config import SETTINGS


def plan_instagram(angle: str) -> str:
    """Instagram Graph posting requires a Business/Creator account.

    This tool only returns a carousel/reel plan. Live publishing stays off
    unless ALLOW_LIVE_POSTS is true AND a human confirms in the CLI.
    """
    angle = angle.strip() or "beginner-friendly tip carousel"
    status = "connected" if SETTINGS.instagram_access_token else "planning-only (no token)"
    live = "blocked" if not SETTINGS.allow_live_posts else "still requires explicit CLI confirm"
    return (
        f"Instagram mode={status}; publish={live}. "
        f"Angle: {angle}. Suggest a 5-slide carousel: 1 hook, 2-4 steps, 5 saveable recap. "
        "Caption under 150 words plus 5-8 relevant tags. No engagement pods or fake likes."
    )
