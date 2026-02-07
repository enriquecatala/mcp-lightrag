from enum import Enum


class CancelPipelineResponseStatus(str, Enum):
    CANCELLATION_REQUESTED = "cancellation_requested"
    NOT_BUSY = "not_busy"

    def __str__(self) -> str:
        return str(self.value)
