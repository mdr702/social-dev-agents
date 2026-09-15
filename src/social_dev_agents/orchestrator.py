from __future__ import annotations

from datetime import date

from social_dev_agents.config import SETTINGS
from social_dev_agents.models import CampaignBrief, CampaignPack, PlatformDraft
from social_dev_agents.safety import check_topic, family_guard, sanitize_hashtags
from social_dev_agents.tools import lookup_github_repo, lookup_x_topic, lookup_youtube, plan_instagram


def research(brief: CampaignBrief) -> dict[str, str]:
    notes: dict[str, str] = {}
    if "github" in brief.platforms and brief.github_repo:
        notes["github"] = lookup_github_repo(brief.github_repo)
    if "youtube" in brief.platforms:
        notes["youtube"] = lookup_youtube(brief.youtube_query or brief.topic)
    if "x" in brief.platforms:
        notes["x"] = lookup_x_topic(brief.x_query or brief.topic)
    if "instagram" in brief.platforms:
        notes["instagram"] = plan_instagram(brief.instagram_angle or brief.topic)
    return notes


def _drafts_from_template(brief: CampaignBrief, research_notes: dict[str, str]) -> list[PlatformDraft]:
    topic = brief.topic.strip()
    tags = sanitize_hashtags(
        ["LearnInPublic", "GitHub", "YouTube", "BuildInPublic", "Students", "Coding"]
    )
    drafts: list[PlatformDraft] = []

    if "github" in brief.platforms:
        drafts.append(
            PlatformDraft(
                platform="github",
                title=f"README section: {topic}",
                body=(
                    f"## Why this exists\n{topic} for {brief.audience}.\n\n"
                    f"## Quick start\n1. Fork or copy the template.\n2. Change the README.\n"
                    f"3. Make one small commit.\n\n"
                    f"Research note: {research_notes.get('github', 'n/a')}"
                ),
                assets=["README.md"],
                cta="Open an issue if you get stuck.",
                notes="Writes nothing to GitHub. Copy into your repo yourself.",
            )
        )
    if "youtube" in brief.platforms:
        drafts.append(
            PlatformDraft(
                platform="youtube",
                title=f"{topic} (beginner walkthrough)",
                body=(
                    f"Hook: '{topic}' in plain words.\n"
                    f"Chapters: 0:00 what/why, 0:30 demo, 2:00 common mistake, 3:00 recap.\n"
                    f"Description: who this is for ({brief.audience}), tools needed, links.\n"
                    f"Research note: {research_notes.get('youtube', 'n/a')}"
                ),
                hashtags=tags[:4],
                assets=["thumbnail idea: big readable title, no clutter"],
                cta="One next video only.",
            )
        )
    if "x" in brief.platforms:
        drafts.append(
            PlatformDraft(
                platform="x",
                title=f"Thread: {topic}",
                body=(
                    f"1/ {topic} — a short thread for {brief.audience}.\n"
                    f"2/ Do the smallest version first. One file, one commit, one post.\n"
                    f"3/ Write down the error you hit. That note helps the next person.\n"
                    f"4/ What part should I unpack next?\n"
                    f"Research note: {research_notes.get('x', 'n/a')}"
                ),
                hashtags=tags[:3],
                cta="Reply with your first repo name.",
            )
        )
    if "instagram" in brief.platforms:
        drafts.append(
            PlatformDraft(
                platform="instagram",
                title=f"Carousel: {brief.instagram_angle or topic}",
                body=(
                    f"Slide 1: {topic}\n"
                    f"Slide 2: Who it's for — {brief.audience}\n"
                    f"Slide 3: Step 1\nSlide 4: Step 2\nSlide 5: Save this checklist\n\n"
                    f"Caption: {topic}. Save this if you are just starting.\n"
                    f"Research note: {research_notes.get('instagram', 'n/a')}"
                ),
                hashtags=tags,
                assets=["1080x1350 slides", "high contrast text"],
                cta="Save + share with a classmate.",
            )
        )
    return drafts


def run_lite(brief: CampaignBrief) -> CampaignPack:
    blocked = check_topic(brief.topic + " " + brief.instagram_angle)
    if blocked:
        return CampaignPack(
            brief=brief,
            safety_review=f"Stopped. Unsafe or off-limits topic ({', '.join(blocked)}).",
            mode="blocked",
        )

    notes = research(brief)
    drafts = _drafts_from_template(brief, notes)
    for draft in drafts:
        draft.body = family_guard(draft.body)

    review = (
        f"Safety review {date.today().isoformat()}: family-friendly={SETTINGS.family_friendly}, "
        f"live posts allowed={SETTINGS.allow_live_posts}. "
        "All outputs are drafts. Humans post manually."
    )
    return CampaignPack(brief=brief, research=notes, drafts=drafts, safety_review=review, mode="lite")
