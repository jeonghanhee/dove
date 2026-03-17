import asyncio
import json
import threading
import websockets
from src.config_loader import WS_URL

class WsClient:
    def __init__(self):
        self._ws = None
        self._loop = None
        self._thread = None
        self._running = False
        self._message_handler = None

    def on_message(self, handler):
        self._message_handler = handler

    def start(self):
        self._running = True
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._connect())

    async def _connect(self):
        while self._running:
            try:
                async with websockets.connect(WS_URL) as ws:
                    self._ws = ws
                    print(f"Connected: {WS_URL}")
                    await self._receive_loop(ws)
            except websockets.ConnectionClosed as e:
                print(f"Connection termination: {e} — Reconnect in 3 seconds")
            except Exception as e:
                print(f"Error: {e} — Reconnect in 3 seconds")
            finally:
                self._ws = None

            if self._running:
                await asyncio.sleep(3)

    async def _receive_loop(self, ws):
        async for raw in ws:
            try:
                message = json.loads(raw)
            except json.JSONDecodeError:
                message = {"raw": raw}

            if self._message_handler:
                self._message_handler(message)

    def send(self, data: dict):
        if self._loop and self._ws:
            asyncio.run_coroutine_threadsafe(self._send(data), self._loop)

    async def _send(self, data: dict):
        if self._ws:
            await self._ws.send(json.dumps(data, ensure_ascii=False))
            
    def stop(self):
        self._running = False
        if self._loop and self._ws:
            asyncio.run_coroutine_threadsafe(self._ws.close(), self._loop)
        print("Terminated")