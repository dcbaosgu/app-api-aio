from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:
    @staticmethod
    def AccountExisted(data: str = ""):
        return StandardException(
            type="users/warning/account-existed",
            status=status.HTTP_400_BAD_REQUEST,
            title="Account already exists.",
            detail=f"The account `{data}` is already used by another user."
        )

    @staticmethod
    def InvalidUserId():
        return StandardException(
            type="users/error/invalid-id",
            status=status.HTTP_404_NOT_FOUND,
            title="User not found",
            detail="User ID provided does not exist in the system."
        )