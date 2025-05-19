from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router
from app.services.websocket import manager
from fastapi.websockets import WebSocketDisconnect
from fastapi.staticfiles import StaticFiles  # Importación añadida
import json
import uvicorn
import os
from app.core.config import settings

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

app.include_router(api_router, prefix="/api")

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)
            await manager.broadcast(
                message=data_json["message"],
                sender=username,
                receiver=data_json["receiver"]
            )
    except WebSocketDisconnect:
        manager.disconnect(username)
    except json.JSONDecodeError:
        await websocket.send_text("Error: Formato de mensaje inválido")

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)