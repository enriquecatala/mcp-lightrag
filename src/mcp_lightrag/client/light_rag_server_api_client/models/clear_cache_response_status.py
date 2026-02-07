from enum import Enum


class ClearCacheResponseStatus(str, Enum):
    FAIL = "fail"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
