from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:
    @staticmethod
    def UserNotFound():
        return StandardException(
            type="user/not-found",
            status=status.HTTP_404_NOT_FOUND,
            title="User not found",
            detail="The specified user does not exist."
        )

    @staticmethod
    def ChannelNotFound():
        return StandardException(
            type="channel-not-found",
            status=status.HTTP_404_NOT_FOUND,
            title="Channel not found",
            detail="The specified chat channel does not exist."
        )
    
    @staticmethod
    def InvalidMembers():
        return StandardException(
            type="channel/invalid-members",
            status=status.HTTP_400_BAD_REQUEST,
            title="Invalid members",
            detail="A chat channel must contain at least 2 members."
        )

    @staticmethod
    def ChannelExist():
        return StandardException(
            type="channel/already-exists",
            status=status.HTTP_409_CONFLICT,
            title="Channel already exists",
            detail="A chat channel with the same members already exists."
        )