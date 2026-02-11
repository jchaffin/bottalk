"""
Launcher — creates a Daily room, starts Sarah and Mike as separate processes,
and auto-opens a browser page that plays the conversation audio.

    python main.py
"""

import asyncio
import http.server
import os
import subprocess
import sys
import threading
import time
import webbrowser
from urllib.parse import urlencode

import aiohttp
from dotenv import load_dotenv
from loguru import logger

from pipecat.transports.daily.utils import (
    DailyRESTHelper,
    DailyRoomParams,
    DailyRoomProperties,
)

load_dotenv(".env.local", override=True)

logger.remove(0)
logger.add(sys.stderr, level="DEBUG", filter=lambda r: "rtvi" not in r["name"])

DURATION = int(os.getenv("CONVERSATION_DURATION", "180"))
TOPIC = os.getenv("CONVERSATION_TOPIC", "enterprise software sales")
HERE = os.path.dirname(os.path.abspath(__file__))
PLAYGROUND_PORT = 8765


def start_playground_server():
    """Serve playground.html on localhost."""
    handler = http.server.SimpleHTTPRequestHandler
    httpd = http.server.HTTPServer(("127.0.0.1", PLAYGROUND_PORT), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd


async def create_room(session: aiohttp.ClientSession):
    key = os.getenv("DAILY_API_KEY")
    if not key:
        raise SystemExit("Set DAILY_API_KEY in .env.local")
    helper = DailyRESTHelper(daily_api_key=key, aiohttp_session=session)
    room = await helper.create_room(
        DailyRoomParams(properties=DailyRoomProperties(exp=time.time() + 600))
    )
    t_sarah = await helper.get_token(room.url)
    t_mike = await helper.get_token(room.url)
    t_browser = await helper.get_token(room.url)
    return room.url, t_sarah, t_mike, t_browser


async def main():
    for k in ("DAILY_API_KEY", "OPENAI_API_KEY", "ELEVENLABS_API_KEY"):
        if not os.getenv(k):
            raise SystemExit(f"Missing {k} — set it in .env.local")

    # Start local web server
    httpd = start_playground_server()

    async with aiohttp.ClientSession() as session:
        room_url, t_sarah, t_mike, t_browser = await create_room(session)

    logger.info(f"Room: {room_url}")
    logger.info(f"Topic: {TOPIC} | Duration: {DURATION}s")

    # Open playground in browser
    qs = urlencode({"roomUrl": room_url, "token": t_browser})
    playground_url = f"http://127.0.0.1:{PLAYGROUND_PORT}/playground.html?{qs}"
    logger.info(f"Opening playground: {playground_url}")
    webbrowser.open(playground_url)

    py = sys.executable

    # Sarah joins first
    proc_sarah = subprocess.Popen(
        [py, os.path.join(HERE, "sarah.py"),
         "--room-url", room_url, "--token", t_sarah],
    )

    # Give Sarah a moment, then Mike joins
    await asyncio.sleep(3)

    proc_mike = subprocess.Popen(
        [py, os.path.join(HERE, "mike.py"),
         "--room-url", room_url, "--token", t_mike],
    )

    logger.info(f"Sarah PID={proc_sarah.pid}  Mike PID={proc_mike.pid}")

    procs = [proc_sarah, proc_mike]
    try:
        if DURATION > 0:
            await asyncio.sleep(DURATION)
            logger.info(f"Time limit ({DURATION}s) reached — terminating.")
        else:
            while proc_sarah.poll() is None or proc_mike.poll() is None:
                await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        for p in procs:
            if p.poll() is None:
                p.terminate()
        for p in procs:
            p.wait(timeout=10)
        httpd.shutdown()
        logger.info("All processes stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stopped.")
