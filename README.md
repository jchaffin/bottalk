# Bottalk

Live AI voice conversations. Two agents join a WebRTC room and role-play a scenario in real time — sales calls, support tickets, discovery sessions, or anything you describe.

Built with [Pipecat](https://pipecat.ai) + [Daily.co](https://daily.co) + [OpenAI](https://openai.com) + [ElevenLabs](https://elevenlabs.io).

## Repo Structure

This is a monorepo with two git submodules:

```
frontend/   Next.js app — UI, API routes, Prisma DB
agents/     Pipecat voice agents — deployed to Pipecat Cloud
```

## Setup

```bash
git clone --recurse-submodules https://github.com/jchaffin/bottalk.git
cd bottalk
```

### Environment

Create `.env.local` at the root with your API keys:

```env
DAILY_API_KEY=
OPENAI_API_KEY=
ELEVENLABS_API_KEY=
PIPECAT_CLOUD_API_KEY=
```

The frontend and agents each have their own `.env.local` — see their READMEs for details.

### Frontend

```bash
cd frontend
npm install
npm run db:push     # push Prisma schema to Postgres
npm run db:seed     # seed built-in scenarios
```

### Agents (local dev)

```bash
cd agents
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Development

```bash
npm run dev:frontend  # Next.js on :3000
npm run dev:agents    # Python agent server on :8000 (for local dev)
```

## Scripts

All root scripts delegate to `frontend/`:

| Command | What it does |
|---|---|
| `npm run dev` | Start frontend dev server |
| `npm run build` | Production build |
| `npm run db:push` | Push Prisma schema |
| `npm run db:seed` | Seed scenarios |
| `npm run db:studio` | Open Prisma Studio |
| `npm run lint` | ESLint |

## How It Works

1. User picks a scenario or types a custom topic
2. Frontend creates a Daily room and starts two Pipecat agents
3. Each agent runs: audio in → VAD → GPT-4o → ElevenLabs TTS → audio out
4. Browser joins the room as a listener with a live transcript

## Tech

| | |
|---|---|
| Frontend | Next.js 16, React 19, Tailwind v4 |
| Database | Prisma 7, PostgreSQL (Prisma Postgres) |
| Agents | Pipecat, GPT-4o, ElevenLabs, Silero VAD |
| Transport | Daily.co WebRTC, Deepgram transcription |
| Deploy | Vercel (frontend), Pipecat Cloud (agents) |
