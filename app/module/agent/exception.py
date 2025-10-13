from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:
    @staticmethod
    def GeminiError(exception: str):
        return StandardException(
            type="gemini/error/generate-failed",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            title="Gemini Service Error",
            detail=exception or "An error occurred while calling Gemini."
        )

    @staticmethod
    def OpenAIError(exception: str):
        return StandardException(
            type="openai/error/generate-failed",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            title="OpenAI Service Error",
            detail=exception or "An error occurred while calling OpenAI."
        )

    @staticmethod
    def ClaudeError(exception: str):
        return StandardException(
            type="claude/error/generate-failed",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            title="ClaudeAI Service Error",
            detail=exception or "An error occurred while calling CladeAI."
        )
