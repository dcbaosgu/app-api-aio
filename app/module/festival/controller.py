from .service import event_service, ticket_service


class EventController:
    def __init__(self):
        self.service = event_service

    async def create(self, data):
        result = await self.service.create(data)
        return result

    async def get(self, event_id):
        result = await self.service.get(event_id)
        return result
    
    async def update(self, event_id, data):
        result = await self.service.update(event_id, data)
        return result

    async def delete(self, event_id):
        result = await self.service.delete(event_id)
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.service.search(query, page, limit)
        return result


class TicketController:
    def __init__(self):
        self.service = ticket_service

    async def checkout(self, data):
        result = await self.service.checkout(data)
        return result

    async def checkin(self, data):
        result = await self.service.checkin(data)
        return result
    
    async def cofirm_pay(self, ticket_id, status):
        result = await self.service.confirm_pay(ticket_id, status)
        return result
    
    async def search(self, query: dict, page: int, limit: int):
        result = await self.service.search(query, page, limit)
        return result
    
    async def qr_code(self, ticket_id: str, format: str):
        result = await self.service.qr_code(ticket_id, format)
        return result