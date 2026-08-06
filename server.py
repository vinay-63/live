import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

clients: list[WebSocket] = []

async def score_updates():
    scores = [
        {"teamA": "50/1 (6.2)", "teamB": "Yet to Bat"},
        {"teamA": "75/2 (10.4)", "teamB": "Yet to Bat"},
        {"teamA": "100/3 (14.6)", "teamB": "Yet to Bat"},
        {"teamA": "120/3 (15.2)", "teamB": "Yet to Bat"},
    ]
    while True:
        for score in scores:
            # Iterate over a copy of the list
            for client in clients.copy():
                try:
                    await client.send_json(score)
                except Exception:
                    # Remove stale clients if sending fails
                    if client in clients:
                        clients.remove(client)
            await asyncio.sleep(5)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Launch background task
    task = asyncio.create_task(score_updates())
    yield
    # Cleanup on shutdown
    task.cancel()

app = FastAPI(lifespan=lifespan)

@app.websocket("/ws/score")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")
            # Broadcast incoming text to all active clients
            for client in clients.copy():
                try:
                    await client.send_text(data)
                except Exception:
                    pass
    except WebSocketDisconnect:
        print("Client disconnected cleanly")
    except Exception as e:
        print(f"Client disconnected with error: {e}")
    finally:
        if websocket in clients:
            clients.remove(websocket)
