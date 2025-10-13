from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:
    @staticmethod
    def GenerateQRFailed():
        return StandardException(
            type="sepay/error/generate-failed",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            title="Sepay Service Error",
            detail="An error occurred while calling Sepay."
        )