import json, aio_pika
from typing import Union
from .config import RABBITMQ_URL, RABBITMQ_QUEUE
from .exception import ErrorCode
from worker.email.service import email_service

class RabbitMQService:
    def __init__(self, queue_name: str = RABBITMQ_QUEUE):
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.email_service = email_service

    async def connect(self):
        try:
            if not self.connection:
                # print(f"[RabbitMQ] Connecting to: {RABBITMQ_URL}")
                self.connection = await aio_pika.connect_robust(RABBITMQ_URL)
                # print("[RabbitMQ] Connection successful.")

                self.channel = await self.connection.channel()
                await self.channel.declare_queue(self.queue_name, durable=True)
                # print(f"[RabbitMQ] Queue declared: {self.queue_name}")

        except Exception as e:
            raise ErrorCode.RabbitConnect()

    async def producer(self, email: str, fullname: str, data: Union[dict, str], mail_type: str):
        
        payload = {"email": email, "fullname": fullname, "data": data, "mail_type": mail_type}
        
        try:
            await self.connect()
            body = json.dumps(payload).encode()
            
            await self.channel.default_exchange.publish(aio_pika.Message(body=body), routing_key=self.queue_name)
            
            # print(f"[RabbitMQ] Published message for {data.email}")
        except Exception as e:
            raise ErrorCode.RabbitProducer()


    async def consumer(self):
        await self.connect()
        queue = await self.channel.declare_queue(self.queue_name, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        payload = json.loads(message.body)

                        if payload.get("mail_type") == "reset_password":
                            await self.email_service.send_otp(
                                email=payload.get("email"), 
                                fullname=payload.get("fullname"), 
                                data=payload.get("data", {}) )

                        elif payload.get("mail_type") == "issue_invoice":
                            await self.email_service.send_invoice(
                                email=payload.get("email"), 
                                fullname=payload.get("fullname"), 
                                data=payload.get("data", {}) )
                        
                        else: raise ErrorCode.InvalidEmailData()

                    except Exception:
                        raise ErrorCode.RabbitConsumer()
  
                    
rabbitmq_service = RabbitMQService()