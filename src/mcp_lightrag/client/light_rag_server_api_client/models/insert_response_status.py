from enum import Enum


class InsertResponseStatus(str, Enum):
    DUPLICATED = "duplicated"
    FAILURE = "failure"
    PARTIAL_SUCCESS = "partial_success"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
