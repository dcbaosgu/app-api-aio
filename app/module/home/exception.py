from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:
    @staticmethod
    def InvalidDateFormat():
        return StandardException(
            type="validation/error/invalid-date-format",
            status=status.HTTP_400_BAD_REQUEST,
            title="Invalid date format",
            detail=f"Field must follow format (e.g., 01/10/2025)."
        )
    
    def BackupDatabaseFailed():
        return StandardException(
            type="database/error/backup-failed",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            title="Database backup failed",
            detail="An error occurred while exporting or backing up the database. Please try again later."
        )
