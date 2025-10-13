from typing import Dict, Tuple
from . import schema
from app.mongo.base import BaseCRUD
from app.mongo.engine import engine_aio
from app.utils.helper import Helper
from .exception import ErrorCode

channel_crud = BaseCRUD("chat-channel", engine_aio)
message_crud = BaseCRUD("chat-message", engine_aio)


class SocketServices:
    def __init__(self, channel_crud: BaseCRUD, message_crud: BaseCRUD):
        self.channel_crud = channel_crud
        self.message_crud = message_crud
        self.active_connections: Dict[str, list[Tuple[any, str]]] = {}

    async def _validate_user_in_channel(self, channel_id: str, token: str):
        try:
            payload = await Helper.decode_access_token(token)
            user_id = payload.get("uid")
        except Exception:
            raise ErrorCode.UserNotFound()

        channel = await self.channel_crud.get_by_id(channel_id)
        if not channel:
            raise ErrorCode.ChannelNotFound()

        if user_id not in channel.get("members", []):
            raise ErrorCode.UserNotFound()

        return user_id, channel

    async def connect(self, channel_id: str, websocket, token: str):
        # Validate & add connect in list
        user_id, _ = await self._validate_user_in_channel(channel_id, token)
        await websocket.accept()
        self.active_connections.setdefault(channel_id, []).append((websocket, user_id))
        # print(f"[CONNECT] Channel {channel_id}: now {len(self.active_connections[channel_id])} connections.")

    def disconnect(self, channel_id: str, websocket):
        # Delete connect WebSocket
        if channel_id in self.active_connections:
            self.active_connections[channel_id] = [
                (ws, uid) for (ws, uid) in self.active_connections[channel_id] if ws != websocket
            ]
            if not self.active_connections[channel_id]:
                del self.active_connections[channel_id]

    async def broadcast(self, channel_id: str, message: dict, members: list):
        # Send message to all websocket for member
        for ws, uid in self.active_connections.get(channel_id, []).copy():
            if uid not in members:
                continue
            try:
                await ws.send_json(message)
            except Exception:
                self.active_connections[channel_id].remove((ws, uid))

    async def send_message(self, data: dict, token: str) -> dict:
        sender_id, channel = await self._validate_user_in_channel(data["channel_id"], token)

        chat_message = schema.ChatMessages(
            channel_id=data["channel_id"],
            sender=sender_id,
            content=data["content"],
            type=data.get("type", "text"),
            status="sent",
            created_at=Helper.get_timestamp(),
        )
        await self.message_crud.create(chat_message.dict())

        last_message = schema.LastMessenge(sender=sender_id, content=data["content"])
        await self.channel_crud.update_by_id(channel["_id"], {"last_message": last_message.dict()})

        await self.broadcast(data["channel_id"], chat_message.dict(), channel["members"])
        return chat_message.dict()


    async def create(self, data: dict):
        members = data.get("members", [])
        if not members or len(members) < 2:
            raise ErrorCode.InvalidMembers()
        
        query = {
            "members": {"$all": members},
            "members": {"$size": len(members)}
        }
        list_channel = await self.channel_crud.search(page=1, limit=10000, query=query)

        for channel in list_channel["results"]:
            if set(channel["members"]) == set(members):
                raise ErrorCode.ChannelExist()

        result = await self.channel_crud.create(data)
        return result
    

socket_service = SocketServices(channel_crud, message_crud)