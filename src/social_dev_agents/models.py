from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Platform = Literal["instagram", "youtube", "x", "github"]


class CampaignBrief(BaseModel):
    topic: str
    audience: str = "general beginners"
    tone: str = "friendly and clear"
    github_repo: str = ""
    youtube_query: str = ""
    x_query: str = ""
    instagram_angle: str = ""
    platforms: list[Platform] = Field(default_factory=lambda: ["github", "youtube", "x", "instagram"])


class PlatformDraft(BaseModel):
    platform: Platform
    title: str
    body: str
    hashtags: list[str] = Field(default_factory=list)
    assets: list[str] = Field(default_factory=list)
    cta: str = ""
    notes: str = "Draft only. Review before posting."


class CampaignPack(BaseModel):
    brief: CampaignBrief
    research: dict[str, str] = Field(default_factory=dict)
    drafts: list[PlatformDraft] = Field(default_factory=list)
    safety_review: str = ""
    mode: str = "lite"
