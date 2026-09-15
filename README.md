# Social + Dev Agent Crew

Live repo: https://github.com/mdr702/social-dev-agents

Get a free AI key (no card): see [FREE_TOKENS.md](FREE_TOKENS.md).

Multi-agent toolkit that plans **family-friendly** content for:

- GitHub (README / repo notes)
- YouTube (title, chapters, description)
- X (short thread)
- Instagram (carousel plan)

It uses three orchestration styles you can switch between:

| Engine | File | What it is |
| --- | --- | --- |
| Lite (always works) | `src/social_dev_agents/orchestrator.py` | Built-in crew: research → draft → safety |
| CrewAI | `src/social_dev_agents/crews/content_crew.py` | Researcher + writer + safety editor |
| LangGraph | `src/social_dev_agents/graphs/campaign_graph.py` | State graph: safety → research → draft |
| OpenAI Agents SDK | `src/social_dev_agents/openai_style/router.py` | Handoff router across 4 specialists |

Nothing is posted automatically. `ALLOW_LIVE_POSTS` stays false.

## Quick start

```bash
cd social-dev-agents
python3 -m venv .venv
source .venv/bin/activate
pip install python-dotenv pydantic httpx rich typer
export PYTHONPATH=src
python main.py demo
```

Optional full stack:

```bash
pip install -r requirements.txt
cp .env.example .env
# add GROQ_API_KEY or GEMINI_API_KEY and any platform keys
python main.py plan --topic "first pull request" --github-repo "octocat/Hello-World" --engine langgraph
```

## Commands

```bash
python main.py demo
python main.py plan --topic "how to write a README" --audience "new students" --engine lite
python main.py from-json examples/sample_brief.json --engine crewai
```

## Safety rules baked in

- School-safe / family-friendly copy
- No fake followers, engagement pods, or private scraping
- GitHub tool is **read-only**
- YouTube search uses `safeSearch=strict` when a key is present
- Instagram / X tools draft only unless you later add a confirmed publish step

## Project layout

```
src/social_dev_agents/
  orchestrator.py      lite crew
  crews/               CrewAI
  graphs/              LangGraph
  openai_style/        OpenAI Agents SDK
  tools/               github, youtube, x, instagram
```
