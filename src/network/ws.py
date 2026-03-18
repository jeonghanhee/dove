import asyncio
import json
import threading
import time
import websockets
from src.config_loader import WS_URL 
from .packets import PacketFactory

class WsClient:
    def __init__(self, auth_token=None, client_id=None):
        self._ws = None
        self._loop = None
        self._thread = None
        self._running = False
        self._message_handler = None
        self.auth_token = auth_token
        self.client_id = client_id
        self._heartbeat_task = None

    def on_message(self, handler):
        self._message_handler = handler

    def start(self):
        if self._running: return
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
                headers = {"Authorization": f"Bearer {self.auth_token}"} if self.auth_token else {}

                async with websockets.connect(WS_URL, additional_headers=headers) as ws:
                    self._ws = ws
                    print("Connected")
                    self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
                    await self._receive_loop(ws)
            except Exception as e:
                print(f"Connection error: {e}")
            finally:
                if self._heartbeat_task:
                    self._heartbeat_task.cancel()
                    self._heartbeat_task = None
                self._ws = None

            if self._running:
                print("Try to reconnect after 3 seconds.")
                await asyncio.sleep(3)

    async def _heartbeat_loop(self):
        try:
            while self._running and self._ws:
                await self._send(PacketFactory.heartbeat())
                await asyncio.sleep(30)
        except asyncio.CancelledError:
            pass

    async def _receive_loop(self, ws):
        async for raw in ws:
            try:
                data = json.loads(raw)
                msg_type = data.get("type")
                
                if msg_type == "receive_tube":
                    print(f"[Receive_Tube] {data['sender']}'s Message: {data['content']}")
                elif msg_type == "server_notification":
                    print(f"[Server_Notification] {data['alert']}")
                    
                if self._message_handler:
                    self._message_handler(data)
            except json.JSONDecodeError:
                pass
            
    def send_tube(self, destination: str, content: str):
        payload = PacketFactory.send_tube(
            origin=self.client_id, 
            destination=destination, 
            content=content
        )
        self.send(payload)

    def send(self, data: dict):
        if self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(self._send(data), self._loop)

    async def _send(self, data: dict):
        if self._ws:
            try:
                await self._ws.send(json.dumps(data, ensure_ascii=False))
            except Exception as e:
                print(f"Send Error: {e}")

    def stop(self):
        self._running = False
        if self._loop:
            self._loop.call_soon_threadsafe(self._loop.stop)
        print("Terminated")