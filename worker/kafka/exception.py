from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:

    @staticmethod
    def KafkaSendFailed():
        return StandardException(
            type="kafka/producer/send-failed",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            title="Kafka Send Failed",
            detail="Failed to send message to Kafka topic."
        )

    @staticmethod
    def KafkaMessageProcessingFailed():
        return StandardException(
            type="kafka/consumer/message-processing-failed",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            title="Kafka Message Processing Failed",
            detail="Failed to process incoming Kafka message."
        )

    @staticmethod
    def KafkaConsumerFatalError():
        return StandardException(
            type="kafka/consumer/fatal-error",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            title="Kafka Consumer Fatal Error",
            detail="Fatal error occurred while consuming messages."
        )
