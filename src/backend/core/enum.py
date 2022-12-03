import enum
import typing as tp


class Enum(enum.Enum):
    @classmethod
    def values(cls) -> list[tp.Any]:
        return [e.value for e in cls]
