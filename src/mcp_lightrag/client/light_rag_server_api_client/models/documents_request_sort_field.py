from enum import Enum


class DocumentsRequestSortField(str, Enum):
    CREATED_AT = "created_at"
    FILE_PATH = "file_path"
    ID = "id"
    UPDATED_AT = "updated_at"

    def __str__(self) -> str:
        return str(self.value)
