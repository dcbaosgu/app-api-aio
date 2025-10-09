from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:
    @staticmethod
    def SubjectExisted(data: str = ""):
        return StandardException(
            type="subject/warning/subject-existed",
            status=status.HTTP_400_BAD_REQUEST,
            title="Subject name already exists.",
            detail=f"The subject or key name `{data}` is duplicate in system."
        )
    
    @staticmethod
    def InvalidAPIKeyId():
        return StandardException(
            type="apikey/error/invalid-id",
            status=status.HTTP_404_NOT_FOUND,
            title="API Key not found",
            detail="API Key ID provided does not exist in the system."
        )