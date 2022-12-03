import typing as tp
from .types import TJsonSerializable


T = tp.TypeVar("T", bound="DataClass")


def dataclass(_cls: tp.Type[T], *args, **kwargs) -> tp.Type[T]:
    """ Wrapper of marshmallow_dataclass.dataclass for original class type hints. """
    return marshmallow_dataclass.dataclass(_cls, *args, **kwargs)
import abc
import dataclasses
import typing as tp
import dataclasses

import marshmallow as msh
import marshmallow_dataclass


class DataClassMeta(abc.ABCMeta):
    """ Loads protobuf message class and wraps in marshmallow_dataclass.dataclass on class defenition. """

    def __new__(
        metacls,
        name: str,
        bases: tp.Tuple[type],
        attrs: dict,
    ):
        return dataclass(_cls=super().__new__(metacls, name, bases, attrs))


class DataClass(metaclass=DataClassMeta):
    Schema: tp.ClassVar[tp.Type[msh.Schema]] = msh.Schema

    class Meta:
        # options: https://marshmallow.readthedocs.io/en/stable/api_reference.html#marshmallow.Schema.Meta
        unknown = msh.RAISE

    def to_dict(self, validate=True) -> TJsonSerializable:
        if validate:
            return self.Schema().dump(self)
        return dataclasses.asdict(self)

    @classmethod
    def load(cls: tp.Type[T], msg: dict, unknown: tp.Optional[str] = None) -> T:
        return cls.Schema(unknown=(unknown or cls.Meta.unknown)).load(msg)