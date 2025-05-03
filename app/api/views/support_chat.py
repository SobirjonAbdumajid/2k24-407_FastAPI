from fastapi import APIRouter
from starlette.websockets import WebSocket

router = APIRouter()

@router.websocket("/ws/")
async def support_chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    async for message in websocket.iter_text():
        await websocket.send_text(f"Message text was: {message}")