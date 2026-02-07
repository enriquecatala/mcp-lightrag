from enum import Enum


class QueryRequestMode(str, Enum):
    BYPASS = "bypass"
    GLOBAL = "global"
    HYBRID = "hybrid"
    LOCAL = "local"
    MIX = "mix"
    NAIVE = "naive"

    def __str__(self) -> str:
        return str(self.value)
