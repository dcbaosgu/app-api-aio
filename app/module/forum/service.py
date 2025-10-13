from app.mongo.base import BaseCRUD
from app.mongo.engine import engine_aio
from app.module.user.service import user_crud
from .exception import ErrorCode

thread_crud = BaseCRUD("forum-thread", engine_aio)
post_crud = BaseCRUD("forum-post", engine_aio)


class ThreadService:
    def __init__(self, thread_crud: BaseCRUD):
        self.thread_crud = thread_crud
        self.user_crud = user_crud

    async def create(self, data: dict):
        user = await self.user_crud.get_by_id(data["author_id"])
        
        if not user: raise ErrorCode.UserNotFound()

        result = await self.thread_crud.create(data)
        return result

    async def get(self, thread_id: str):  
        result = await self.thread_crud.get_by_id(thread_id)

        if not result: raise ErrorCode.ThreadNotFound()
        return result

    async def update(self, thread_id: str, data: dict):
        result = await self.thread_crud.update_by_id(thread_id, data)
        if not result:
            raise ErrorCode.ThreadNotFound()
        return result

    async def delete(self, thread_id: str):
        result = await self.thread_crud.delete_by_id(thread_id)
        if not result:
            raise ErrorCode.ThreadNotFound()
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.thread_crud.search(query, page, limit)
        return result


class PostService:
    def __init__(self, post_crud: BaseCRUD, thread_crud: BaseCRUD):
        self.post_crud = post_crud
        self.thread_crud = thread_crud
        self.user_crud = user_crud

    async def create(self, data: dict):

        thread = await self.thread_crud.get_by_id(data["thread_id"])
        user = await self.user_crud.get_by_id(data["author"]["user_id"])

        if not thread: raise ErrorCode.ThreadNotFound()
        if not user: raise ErrorCode.UserNotFound()

        await self.thread_crud.update_one_nomit({"_id": thread["_id"]}, {"$inc": {"comments": 1}})

        result = await self.post_crud.create(data)
        return result

    async def get(self, post_id: str):
        result = await self.post_crud.get_by_id(post_id)
        if not result:
            raise ErrorCode.PostNotFound()
        return result

    async def update(self, post_id: str, data: dict):
        result = await self.post_crud.update_by_id(post_id, data)
        if not result:
            raise ErrorCode.PostNotFound()
        return result

    async def delete(self, post_id: str):
        post = await self.post_crud.get_by_id(post_id)
        if not post: 
            raise ErrorCode.PostNotFound()

        thread = await self.thread_crud.get_by_id(post.get("thread_id"))
        if thread: 
            await self.thread_crud.update_one_nomit({"_id": thread["_id"]}, {"$inc": {"comments": -1}})

        result = await self.post_crud.delete_by_id(post_id)
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.post_crud.search(query, page, limit)
        return result

    async def reaction(self, post_id: str, reaction: str, user_id: str):
        post = await self.post_crud.get_by_id(post_id)
        if not post:
            raise ErrorCode.PostNotFound()

        reactions = post.get("reactions", {})

        # Check exist Reaction for User
        user_already_reacted = user_id in reactions.get(reaction, [])

        # If again reaction -> Remove
        if user_already_reacted:
            reactions[reaction].remove(user_id)
            
            # Delete Reaction empty
            if not reactions[reaction]:
                del reactions[reaction]
        else:
            # Delete reaction old & add reaction new
            for rtype, users in reactions.items():
                if user_id in users:
                    reactions[rtype].remove(user_id)

            reactions.setdefault(reaction, []).append(user_id)

        await self.post_crud.update_by_id(post["_id"], {"reactions": reactions})
        return {"post_id": post_id, "reactions": reactions}


thread_service = ThreadService(thread_crud)
post_service = PostService(post_crud=post_crud, thread_crud=thread_crud)