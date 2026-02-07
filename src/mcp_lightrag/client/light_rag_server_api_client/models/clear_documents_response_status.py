from enum import Enum


class ClearDocumentsResponseStatus(str, Enum):
    BUSY = "busy"
    FAIL = "fail"
    PARTIAL_SUCCESS = "partial_success"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
