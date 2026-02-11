# Two AI Voice Agents Talking to Each Other

Two Pipecat voice agents that join the same Daily.co WebRTC room and have a natural, real-time conversation about a configurable topic (default: enterprise software sales).

| Agent   | Role                      | Voice        |
|---------|---------------------------|--------------|
| Sarah   | Sales rep (TechFlow Solutions) | Rachel (ElevenLabs) |
| Mike    | VP of Ops (BrightCart)    | Josh (ElevenLabs)   |

## How It Works

1. A Daily.co room is created via the REST API.
2. Two Pipecat pipelines join the room as separate participants.
3. Each pipeline: **receives audio** → **Daily transcription (Deepgram)** → **OpenAI GPT-4o** → **ElevenLabs TTS** → **sends audio back**.
4. Sarah speaks first; Mike listens, then responds. The conversation flows naturally.

## Prerequisites

- **Python 3.11+**
- **Daily.co account** — sign up at <https://dashboard.daily.co> and grab an API key.
- **OpenAI API key** — <https://platform.openai.com/api-keys>
- **ElevenLabs API key** — <https://elevenlabs.io>

## Setup

```bash
# 1. Create a virtual environment
python -m venv .venv && source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
#    Edit .env.local and fill in your keys:
#      DAILY_API_KEY=...
#      OPENAI_API_KEY=...
#      ELEVENLABS_API_KEY=...
```

## Usage

```bash
python main.py
```

The conversation runs for 180 seconds by default. Press `Ctrl+C` to stop early.

### Environment Variables

| Variable                | Default                        | Description                         |
|-------------------------|--------------------------------|-------------------------------------|
| `DAILY_API_KEY`         | *(required)*                   | Daily.co API key                    |
| `OPENAI_API_KEY`        | *(required)*                   | OpenAI API key                      |
| `ELEVENLABS_API_KEY`    | *(required)*                   | ElevenLabs API key                  |
| `CONVERSATION_TOPIC`    | `enterprise software sales`    | Topic the agents discuss            |
| `CONVERSATION_DURATION` | `180`                          | Max conversation length in seconds (0 = unlimited) |
| `SARAH_VOICE_ID`        | `21m00Tcm4TlvDq8ikWAM`        | ElevenLabs voice ID for Sarah       |
| `MIKE_VOICE_ID`         | `TxGEqnHWrfWFTfGW9XjX`        | ElevenLabs voice ID for Mike        |
