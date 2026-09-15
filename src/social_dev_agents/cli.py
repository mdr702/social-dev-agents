from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from social_dev_agents.models import CampaignBrief, CampaignPack
from social_dev_agents.orchestrator import run_lite

app = typer.Typer(add_completion=False, no_args_is_help=True)
console = Console()


def _print_pack(pack: CampaignPack) -> None:
    console.print(Panel(pack.safety_review or "No review", title=f"mode={pack.mode}"))
    if pack.research:
        table = Table(title="Research")
        table.add_column("Platform")
        table.add_column("Notes")
        for key, value in pack.research.items():
            table.add_row(key, value[:400])
        console.print(table)
    for draft in pack.drafts:
        console.print(
            Panel(
                f"[bold]{draft.title}[/bold]\n\n{draft.body}\n\n"
                f"Tags: {' '.join('#' + t for t in draft.hashtags)}\n"
                f"CTA: {draft.cta}\nNote: {draft.notes}",
                title=draft.platform,
            )
        )


def _save(pack: CampaignPack) -> Path:
    from social_dev_agents.config import SETTINGS

    path = SETTINGS.output_dir / "last_campaign.json"
    path.write_text(pack.model_dump_json(indent=2), encoding="utf-8")
    return path


@app.command()
def demo() -> None:
    """Run the bundled beginner-repo sample with live GitHub public lookup."""
    sample = Path(__file__).resolve().parents[2] / "examples" / "sample_brief.json"
    brief = CampaignBrief.model_validate_json(sample.read_text(encoding="utf-8"))
    pack = run_lite(brief)
    _print_pack(pack)
    saved = _save(pack)
    console.print(f"Saved {saved}")


@app.command()
def plan(
    topic: str = typer.Option(..., help="What the campaign is about"),
    audience: str = typer.Option("students learning to code"),
    github_repo: str = typer.Option("", help="owner/name"),
    engine: str = typer.Option("lite", help="lite | crewai | langgraph | openai"),
) -> None:
    """Build drafts. Never publishes."""
    brief = CampaignBrief(
        topic=topic,
        audience=audience,
        github_repo=github_repo,
        youtube_query=topic,
        x_query=topic,
        instagram_angle=topic,
    )
    if engine == "crewai":
        from social_dev_agents.crews.content_crew import run_crewai

        pack = run_crewai(brief)
    elif engine == "langgraph":
        from social_dev_agents.graphs.campaign_graph import run_langgraph

        pack = run_langgraph(brief)
    elif engine == "openai":
        from social_dev_agents.openai_style.router import run_openai_agents

        pack = run_openai_agents(brief)
    else:
        pack = run_lite(brief)
    _print_pack(pack)
    console.print(f"Saved {_save(pack)}")


@app.command()
def from_json(
    path: Path = typer.Argument(..., exists=True, readable=True),
    engine: str = typer.Option("lite"),
) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    brief = CampaignBrief.model_validate(data)
    plan(topic=brief.topic, audience=brief.audience, github_repo=brief.github_repo, engine=engine)


if __name__ == "__main__":
    app()
