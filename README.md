# Bottalk

Live AI voice conversations. Two agents join a WebRTC room and role-play a scenario in real time — sales calls, support tickets, discovery sessions, or anything you describe.

Built with [Pipecat](https://pipecat.ai) + [Daily.co](https://daily.co) + [OpenAI](https://openai.com) + [ElevenLabs](https://elevenlabs.io).

## Repo structure

Thin parent repo with two Git submodules:

```
frontend/   Next.js app — UI, API routes, Prisma DB
agents/     Pipecat voice agents — deployed to Pipecat Cloud
```

The root `package.json` only orchestrates local dev; the Next.js app lives under `frontend/`.

## Setup

```bash
git clone --recurse-submodules https://github.com/jchaffin/bottalk.git
cd bottalk
npm install
```

### Submodules

Parent commits **pin** submodule SHAs. A leading `+` in `git submodule status` means your checkout does not match the parent’s recorded commit.

```bash
./scripts/sync-submodules.sh
git add agents frontend && git commit -m "Bump submodules"
```

After a remote URL change: `git submodule sync --recursive`. Track `master` in each submodule: `git submodule update --remote --merge`.

### Environment

Create `.env.local` at the **repo root** for keys shared by tooling, and use each submodule’s `.env.local` for app-specific secrets (see their READMEs).

```env
DAILY_API_KEY=
OPENAI_API_KEY=
ELEVENLABS_API_KEY=
PIPECAT_CLOUD_API_KEY=
PCC_PRIVATE_KEY=
```

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
npm run dev              # kill :3000 if busy, then frontend + agents
npm run dev:frontend     # Next.js on :3000 only
npm run dev:agents       # Python agent server on :8000
```

## Root scripts

| Command | What it does |
|---------|----------------|
| `npm run dev` | Free port 3000, then run frontend and agents together |
| `npm run dev:local` | Same as concurrent dev, without killing :3000 |
| `npm run dev:frontend` | `npm run dev` in `frontend/` |
| `npm run dev:agents` | `dev.py` in `agents/` |
| `npm run build` | Production build (`frontend/`) |
| `npm run db:push` / `db:seed` / `db:studio` | Prisma via `frontend/` |
| `npm run lint` | ESLint in `frontend/` |

## How it works

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
| Deploy | Vercel (`frontend/`), Pipecat Cloud (`agents/`) |

## Vercel (production)

Configure these on the **frontend** Vercel project:

| Variable | Purpose |
|----------|---------|
| `PIPECAT_CLOUD_PUBLIC_API_KEY` | Pipecat Cloud **public** API key — so `/api/start` uses PCC, not localhost |
| `DAILY_API_KEY` | Daily REST API (rooms, tokens) |
| `PRISMA_DATABASE_URL` | Postgres (e.g. Prisma Accelerate) |
| `POSTGRES_URL` | Direct DB URL if you run migrations in CI |

Optional: `PCC_PRIVATE_KEY`, `OPENAI_API_KEY`, etc. — see `frontend` README.

Do not set `NEXT_PUBLIC_API_URL` on Vercel unless you intentionally point the browser at a custom agent URL.
