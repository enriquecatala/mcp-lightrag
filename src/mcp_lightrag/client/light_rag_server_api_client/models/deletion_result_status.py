from enum import Enum


class DeletionResultStatus(str, Enum):
    FAIL = "fail"
    NOT_FOUND = "not_found"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
