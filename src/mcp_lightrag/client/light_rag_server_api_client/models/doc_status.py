from enum import Enum


class DocStatus(str, Enum):
    FAILED = "failed"
    PENDING = "pending"
    PREPROCESSED = "preprocessed"
    PROCESSED = "processed"
    PROCESSING = "processing"

    def __str__(self) -> str:
        return str(self.value)
