# Free AI tokens (no credit card)

Nobody can invent a secret key for you. You create a free key on a real provider, then paste it only into your local `.env` — never into GitHub.

## Fastest options (2026)

1. **Groq** — https://console.groq.com/keys  
   Sign up, create a key, set `GROQ_API_KEY`.  
   Default model: `openai/gpt-oss-20b`.  
   Free tier is rate-limited (about 30 requests/minute, 1,000/day).

2. **Google AI Studio (Gemini)** — https://aistudio.google.com/apikey  
   Create a key, set `GEMINI_API_KEY`.  
   Default model: `gemini-2.0-flash`.

3. **OpenRouter free models** — https://openrouter.ai/settings/keys  
   Set `OPENROUTER_API_KEY`. Use a model id that ends with `:free` when the catalog lists one.

GitHub Models inference was retired on 30 July 2026, so a GitHub login alone is no longer an LLM token.

## Local setup

```bash
cp .env.example .env
# paste ONE key
export PYTHONPATH=src
python main.py plan --topic "first README" --engine lite
```

`python main.py demo` still works with zero keys (templates + public GitHub lookup).
