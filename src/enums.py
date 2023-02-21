from enum import Enum, auto


class GameEntity(Enum):
    CPU = -1
    NOBODY = 0
    USER = 1


class GameSymbol(Enum):
    X = auto()
    O = auto()


class SumGridMappings(Enum):
    ROW = 0
    COL = 1
    DIAG = 2
