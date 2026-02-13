#!/usr/bin/env bash
# Start both the Python agent server and the Next.js frontend.
#
#   ./dev.sh          — start both
#   ./dev.sh stop     — kill background processes started by this script

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
PIDFILE="$ROOT/.dev-pids"

stop() {
  if [[ -f "$PIDFILE" ]]; then
    while read -r pid; do
      kill "$pid" 2>/dev/null || true
    done < "$PIDFILE"
    rm -f "$PIDFILE"
    echo "Stopped dev servers."
  else
    echo "No running dev servers found."
  fi
}

if [[ "${1:-}" == "stop" ]]; then
  stop
  exit 0
fi

# Clean up any previous run
stop 2>/dev/null || true

# ── Python agent server (dev.py on port 8000) ──
echo "Starting Python agent server..."
cd "$ROOT/agents"
if [[ -d "venv" ]]; then
  source venv/bin/activate
fi
python dev.py &
PY_PID=$!
cd "$ROOT"

# ── Next.js frontend (port 3000) ──
echo "Starting Next.js frontend..."
cd "$ROOT/frontend"
npm run dev &
FE_PID=$!
cd "$ROOT"

# Save PIDs for stop command
echo "$PY_PID" > "$PIDFILE"
echo "$FE_PID" >> "$PIDFILE"

echo ""
echo "  Agent server:  http://localhost:8000"
echo "  Frontend:      http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both."

# Forward Ctrl+C to both processes
trap 'stop; exit 0' INT TERM

# Wait for either to exit
wait
