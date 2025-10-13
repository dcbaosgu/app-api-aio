from fastapi import WebSocket, WebSocketDisconnect
from .service import socket_service
from . import schema
from worker.kafka.service import kafka_service

class SocketController:
    def __init__(self):
        self.socket_service = socket_service
        self.kafka_service = kafka_service

    async def chat_realtime(self, channel_id: str, websocket: WebSocket):

        token = websocket.headers.get("Authorization", "").replace("Bearer ", "")
        if not token: return await websocket.close()

        try:
            await self.socket_service.connect(channel_id, websocket, token)
            while True:
                message = schema.MessageSend(**await websocket.receive_json())
                # await self.service.send_message(data={"channel_id": channel_id, **message.dict()}, token=token) # Send direct
                await self.kafka_service.send(channel_id=channel_id, token=token, message=message.model_dump())        # Send queue

        except WebSocketDisconnect:
            print(f"[CONTROLLER] - Client disconnected from {channel_id}")
            
        except Exception as e:
            print(f"[CONTROLLER] - Websocket Close: {e}")
            await websocket.close()

        finally: # Clear memory socket connecting
            self.socket_service.disconnect(channel_id, websocket)

    async def create(self, data):
        result = await self.socket_service.create(data)
        return result
