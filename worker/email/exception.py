from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:

    @staticmethod
    def SendMailFailed():
        return StandardException(
            type="email/error/send-failed",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            title="Email Send Failed",
            detail="Failed to send email. Please try again later."
        )