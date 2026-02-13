# OutRival

Two AI voice agents join a Daily.co WebRTC room and have a real-time conversation powered by OpenAI GPT-4o and ElevenLabs TTS. Pick a built-in scenario or describe your own topic — the agents generate natural, role-played dialogue live.

## Architecture

```
frontend/          Next.js 16 app (React 19, Tailwind v4)
  src/app/api/     API routes — room creation, agent start/stop, scenario CRUD
  src/components/  CallProvider, Transcript, AgentAvatar, ThemeToggle
  prisma/          Prisma schema + seed (Scenario & Session models)

agents/            Pipecat voice agents (deployed to Pipecat Cloud)
  agent.py         Core pipeline: Daily transport → VAD → GPT-4o → ElevenLabs TTS
  bot.py           Pipecat Cloud entry point
  dev.py           Local dev server (FastAPI)
  sarah.py/mike.py CLI wrappers for local runs
```

### How it works

1. **Frontend** — user picks a scenario (from DB) or enters a custom topic. Custom topics go through `/api/generate-prompts` (OpenAI) to create role-specific system prompts.
2. **Start API** — creates a Daily room, generates tokens, and starts two Pipecat Cloud agent sessions (or local subprocesses in dev).
3. **Agents** — each agent joins the room as a separate participant running its own pipeline: audio in → Silero VAD → GPT-4o → ElevenLabs TTS → audio out. Transcription filtering prevents feedback loops.
4. **Browser** — joins the same Daily room as a listener, plays agent audio, and renders a live transcript via custom `bot-llm-text` app-messages.

### Data flow

```
Browser ← Daily room → Agent 1 (Sarah)
                      → Agent 2 (Mike)
                      → Deepgram transcription (shared)
```

## Prerequisites

- **Node.js 20+** and **npm**
- **Python 3.11+** (for local agent development)
- API keys for: [Daily.co](https://dashboard.daily.co), [OpenAI](https://platform.openai.com/api-keys), [ElevenLabs](https://elevenlabs.io)
- [Pipecat Cloud](https://pipecat.daily.co) account (for production agent hosting)
- [Prisma Postgres](https://www.prisma.io/postgres) database (or any PostgreSQL)

## Setup

### 1. Frontend

```bash
cd frontend
npm install

# Configure environment variables
cp .env.local.example .env.local
# Fill in: DAILY_API_KEY, OPENAI_API_KEY, PIPECAT_CLOUD_API_KEY,
#          PRISMA_DATABASE_URL, POSTGRES_URL
```

### 2. Database

```bash
cd frontend

# Push schema to your Prisma Postgres instance
npm run db:push

# Seed the built-in scenarios (sales, support, discovery)
npm run db:seed

# Browse data (optional)
npm run db:studio
```

### 3. Agents (local development)

```bash
cd agents
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Copy env vars
cp ../.env.local .env.local
# Ensure DAILY_API_KEY, OPENAI_API_KEY, ELEVENLABS_API_KEY are set
```

## Development

```bash
# Terminal 1 — frontend
cd frontend && npm run dev

# Terminal 2 — local agent backend (optional, for local dev without Pipecat Cloud)
cd agents && python dev.py
```

When using the local agent backend, set `NEXT_PUBLIC_API_URL=http://localhost:8000` in `frontend/.env.local`.

For production (Pipecat Cloud), leave `NEXT_PUBLIC_API_URL` unset — the frontend API routes handle everything.

## Environment Variables

### Frontend (`frontend/.env.local`)

| Variable | Required | Description |
|---|---|---|
| `DAILY_API_KEY` | Yes | Daily.co API key |
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `PIPECAT_CLOUD_API_KEY` | Yes | Pipecat Cloud public key |
| `PCC_AGENT_NAME` | No | Pipecat Cloud agent name (default: `outrival-agent`) |
| `PRISMA_DATABASE_URL` | Yes | Prisma Accelerate URL (`prisma+postgres://...`) |
| `POSTGRES_URL` | Yes | Direct PostgreSQL URL (for migrations) |
| `NEXT_PUBLIC_API_URL` | No | Set to `http://localhost:8000` for local agent dev |
| `DEFAULT_VOICE_1` | No | ElevenLabs voice ID for agent 1 |
| `DEFAULT_VOICE_2` | No | ElevenLabs voice ID for agent 2 |

### Agents (`agents/.env.local`)

| Variable | Required | Description |
|---|---|---|
| `DAILY_API_KEY` | Yes | Daily.co API key |
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `ELEVENLABS_API_KEY` | Yes | ElevenLabs API key |

## Scenarios

Scenarios are stored in PostgreSQL via Prisma. Each scenario defines two agents with names, roles, voice IDs, and system prompts. The `{{topic}}` placeholder in prompts is replaced at runtime.

Built-in scenarios are seeded via `npm run db:seed`:
- **Enterprise Software Sales** — Sarah pitches, Mike is a skeptical VP
- **Customer Support Call** — Sarah handles a billing complaint
- **Product Discovery Call** — Sarah qualifies a prospect

Users can also enter a custom topic, which generates fresh agent prompts via OpenAI.

## Deployment

**Frontend** — deploy to Vercel. Add all `frontend/.env.local` variables to your Vercel project settings.

**Agents** — pushed to Pipecat Cloud via GitHub Actions on merge to `master`. See `agents/.github/workflows/deploy.yml`.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16, React 19, Tailwind CSS v4 |
| Database | PostgreSQL (Prisma Postgres), Prisma ORM v7 |
| Voice agents | Pipecat, OpenAI GPT-4o, ElevenLabs TTS |
| Real-time | Daily.co WebRTC, Deepgram transcription |
| Hosting | Vercel (frontend), Pipecat Cloud (agents) |
