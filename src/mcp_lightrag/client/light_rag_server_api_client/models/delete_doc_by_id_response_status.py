from enum import Enum


class DeleteDocByIdResponseStatus(str, Enum):
    BUSY = "busy"
    DELETION_STARTED = "deletion_started"
    NOT_ALLOWED = "not_allowed"

    def __str__(self) -> str:
        return str(self.value)
