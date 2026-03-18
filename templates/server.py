import asyncio
import json
import time
import uuid
import uvicorn
import threading
import websockets
from fastapi import FastAPI, HTTPException
from datetime import datetime
from models import LoginRequest, LoginResponse
from token_storage import load_token_storages, save_token_storages

app = FastAPI()

token_storages = load_token_storages()
connected_clients = {}
user_data = {"superadmin": "1234"}

@app.post("/login")
async def login(request: LoginRequest):
    stored_password = user_data.get(request.id)

    if stored_password and stored_password == request.password:
        access_token = f"access_{uuid.uuid4().hex}"
        refresh_token = f"refresh_{uuid.uuid4().hex}"

        token_storages[access_token] = request.id
        save_token_storages(token_storages)

        print(f"[{datetime.now()}] Login Success: {request.id}")
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=3600
        )

    raise HTTPException(status_code=401, detail="Invalid ID or Password")

async def broadcast_periodic_notification():
    while True:
        await asyncio.sleep(30)
        if connected_clients:
            notification = {
                "type": "server_notification",
                "alert": f"System Heartbeat: {time.strftime('%H:%M:%S')}",
                "timestamp": time.time()
            }
            websockets.broadcast(connected_clients.values(), json.dumps(notification, ensure_ascii=False))


async def ws_handler(websocket):
    auth_header = websocket.request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        await websocket.close(1008, "Auth Required")
        return

    token = auth_header.split(" ")[1]
    client_id = token_storages.get(token)

    if not client_id:
        await websocket.close(1008, "Invalid Token")
        return

    connected_clients[client_id] = websocket
    print(f"WebSocket Connected: {client_id}")

    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                if data.get("type") == "heartbeat":
                    await websocket.send(json.dumps({"type": "heartbeat_ack", "timestamp": time.time()}))

                elif data.get("type") == "send_tube":
                    dest = data.get("destination")
                    content = data.get("content", "")

                    packet = {
                        "type": "receive_tube",
                        "sender": client_id,
                        "content": content,
                        "timestamp": time.time()
                    }

                    if dest in connected_clients:
                        await connected_clients[dest].send(json.dumps(packet, ensure_ascii=False))
                        ack = f"Sent to {dest}"
                    else:
                        ack = f"User {dest} offline"

                    await websocket.send(json.dumps({
                        "type": "server_notification", "alert": ack, "timestamp": time.time()
                    }, ensure_ascii=False))
            except json.JSONDecodeError:
                pass
    finally:
        if client_id in connected_clients:
            del connected_clients[client_id]


async def run_ws_server():
    asyncio.create_task(broadcast_periodic_notification())
    async with websockets.serve(ws_handler, "0.0.0.0", 8080):
        await asyncio.Future()

def start_ws_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_ws_server())

if __name__ == "__main__":
    ws_thread = threading.Thread(target=start_ws_thread, daemon=True)
    ws_thread.start()

    uvicorn.run(app, host="0.0.0.0", port=8000)