# Devfolio

Repository for my website.

### Features
- **Voice AI Assistant** - Navigate and ask questions using voice
- **Dynamic Skills** - AI-powered skill categorization
- **Live Projects** - Real-time GitHub integration
- **Interactive Resume** - PDF viewer and download
- **Responsive Design** - Optimized for all devices

## Quick Start

```bash
# Install dependencies
yarn install

# Add environment variables
cp .env.example .env.local
# Add your OPENAI_API_KEY

# Run development server
yarn dev
```

Open [http://localhost:3000](http://localhost:3000)

### Submodules

`frontend` and `agents` are separate GitHub repos; the parent commit pins their SHAs. A leading `+` in `git submodule status` means your checkout does not match the last parent commit.

```bash
./scripts/sync-submodules.sh
git add agents frontend && git commit -m "Bump submodules"
```

Stale remote URLs after a rename: `git submodule sync --recursive`. Update to remote `master`: `git submodule update --remote --merge`.

### Environment

```env
DAILY_API_KEY=
OPENAI_API_KEY=
ELEVENLABS_API_KEY=
PIPECAT_CLOUD_API_KEY=
PCC_PRIVATE_KEY=     # Pipecat Cloud Dashboard > API Keys > Private (for deploy + secrets)
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

## Tech Stack

- Next.js 15 with TypeScript
- Tailwind CSS v4
- OpenAI Agents Framework
- PDF.js for document viewing

## Scripts

- `yarn dev` - Development server
- `yarn build` - Production build
- `yarn lint` - Code linting

---

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

## Vercel (production)

Set these in **Vercel → Project → Settings → Environment Variables** (Production):

| Variable | Purpose |
|----------|---------|
| `PIPECAT_CLOUD_PUBLIC_API_KEY` | Pipecat Cloud **Public** API key — required so `/api/start` talks to PCC instead of localhost |
| `DAILY_API_KEY` | Daily REST API (create rooms, tokens) |
| `PRISMA_DATABASE_URL` | Postgres (Prisma Accelerate URL) |
| `POSTGRES_URL` | Direct DB URL for migrations if you run them in CI |

Optional: `PCC_PRIVATE_KEY` (stop sessions), `OPENAI_API_KEY` (embeddings / KPIs), Pinecone keys.

**Do not** set `NEXT_PUBLIC_API_URL` on Vercel unless you intentionally proxy agents to another URL. Leaving it unset uses Pipecat Cloud when `PIPECAT_CLOUD_PUBLIC_API_KEY` is present.

If calls still fail, check that the PCC agent name matches: `NEXT_PUBLIC_PCC_AGENT_NAME` / `PCC_AGENT_NAME` (default `bottalk-agent`).
