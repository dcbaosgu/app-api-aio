from fastapi import APIRouter, WebSocket
from .controller import SocketController
from . import schema

router = APIRouter(prefix="/socket", tags=["Socket"])
controller = SocketController()


@router.websocket("/ws/{channel_id}")
async def chat_realtime(channel_id: str, websocket: WebSocket):
    await controller.chat_realtime(channel_id, websocket)


@router.post("/create", status_code=201, responses={
                201: {"model": schema.ChannelResponse, "description": "Create items success"}})
async def create_channel(data: schema.ChannelCreate):
    result = await controller.create(data.model_dump())
    return schema.ChannelResponse(**result)