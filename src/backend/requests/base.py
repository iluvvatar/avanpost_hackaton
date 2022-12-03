import dataclasses
import functools
import typing as tp
import dataclasses

import marshmallow as msh
from aiohttp import web
from aiohttp_apispec import docs

from backend.errors import RequestError
from backend.core import DataClass, Enum, TJsonSerializable, THandler, TDecorator


class ERequestLocation(Enum):
    QUERY = "query"
    PATH = "path"
    HEADER = "header"
    BODY = "body"


class RequestSchemaField(msh.fields.Field):

    def FromMsh(self, msh_field: msh.fields.Field, **kwargs) -> dataclasses.field:
        return self.__call__(metadata=dict(marshmallow_field=msh_field), **kwargs)

    def __call__(
        self,
        *args,
        location: ERequestLocation,
        description: str,
        required: bool = False,
        default: tp.Any = dataclasses.MISSING,
        default_factory: tp.Any = dataclasses.MISSING,
        example: TJsonSerializable | None = None,
        metadata: dict | None = None,
        name: str | None = None,
        **kwargs
    ) -> dataclasses.field:
        if required:
            msg = "required request_field shouldn't have default or default_factory specified"
            assert default is dataclasses.MISSING and default_factory is dataclasses.MISSING, msg
        else:
            msg = "request_field can't be required and have default of default_factory specified"
            assert default is not dataclasses.MISSING or default_factory is not dataclasses.MISSING, msg
        metadata = {} if metadata is None else metadata
        metadata["location"] = location
        metadata["required"] = required
        if name:
            metadata["name"] = name
        if example is not None:
            metadata["example"] = example
        metadata = {} if metadata is None else metadata
        metadata.update(kwargs)
        if description:
            metadata["description"] = description
        return dataclasses.field(
            default=default,
            default_factory=default_factory,
            metadata=metadata,
        )


request_field = RequestSchemaField()


T = tp.TypeVar("T", bound="BaseRequest")


class BaseRequest(DataClass):
    @classmethod
    def parse(cls: tp.Type[T], request: web.Request) -> T:
        data = {}
        for field in dataclasses.fields(cls):
            location = field.metadata["location"]
            name = field.metadata["name"] if "name" in field.metadata else field.name
            if location is ERequestLocation.QUERY:
                if name in request.query:
                    data[field.name] = SwaggerType._try_parse_number(request.query.get(name))
            if location is ERequestLocation.PATH:
                data[field.name] = SwaggerType._try_parse_number(request.match_info[name])
            if location is ERequestLocation.HEADER:
                raise NotImplementedError  # TODO
            if location is ERequestLocation.BODY:
                raise NotImplementedError  # TODO

            if field.name in data and SwaggerType.is_swagger_array_type(field.type):
                data[field.name] = SwaggerType.deserialize_array(data[field.name])
            # TODO: if SwaggerType.is_swagger_object_type(field.type):
        try:
            return cls.load(data)
        except msh.ValidationError as exc:
            raise RequestError(msg=str(exc.messages)) from exc


class SwaggerType:
    """ Coverts python type into swagger spec. """

    _PY_TYPE_TO_SWAGGER = {
        int: {"type": "integer", "format": "int32"},
        str: {"type": "string"},
        float: {"type": "number", "format": "float"},
        bool: {"type": "boolean"},
    }

    _DEFAULT_SWAGGER_EXAMPLES = {
        int: 123,
        str: "abc",
        float: 1.23,
        bool: "true",
    }

    def __init__(self, field: dataclasses.Field):
        self.field = field

    @classmethod
    def is_swagger_array_type(cls, t: type) -> bool:
        if cls.is_optional(t):
            t = tp.get_args(t)[0]
        if hasattr(t, "__origin__"):
            t = t.__origin__
        return issubclass(t, tp.Iterable) and not issubclass(t, tp.Mapping) and t is not str

    @classmethod
    def is_swagger_object_type(cls, t: type) -> bool:
        raise NotImplementedError

    @classmethod
    def is_optional(cls, t: type):
        return (tp.get_origin(t) is tp.Union and
                len(tp.get_args(t)) == 2 and
                isinstance(None, tp.get_args(t)[1]))

    @classmethod
    def serialize_array(cls, arr: tp.Iterable) -> str:
        return ",".join(map(str, arr))

    @classmethod
    def deserialize_array(cls, arr: str) -> list[tp.Union[str, int]]:
        arr = arr.split(",") if arr else []
        return [cls._try_parse_number(x) for x in arr]

    @classmethod
    def serialize_object(cls, obj: tp.Mapping) -> str:
        raise NotImplementedError

    @classmethod
    def deserialize_object(cls, obj: str) -> dict[str, str]:
        raise NotImplementedError

    @classmethod
    def _try_parse_number(cls, value: str) -> tp.Union[int, float, str]:
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value

    def swagger(self) -> dict[str, str]:
        parameter = {
            "in": self.field.metadata["location"].value,
            "name": self.field.metadata["name"] if "name" in self.field.metadata else self.field.name,
            "description": self.field.metadata["description"],
            "required": self.field.metadata["required"],
            "example": self.field.metadata["example"] if "example" in self.field.metadata else self._get_example(),
            **self._py_type_to_swagger(self.field.type)
        }
        if not parameter["required"]:
            parameter["default"] = self._get_default_value()
        return parameter

    def _py_type_to_swagger(self, t: type) -> dict[str, str]:
        """ Converts python type to swagger. """

        if self.is_optional(t):
            t = tp.get_args(t)[0]

        if SwaggerType.is_swagger_array_type(t):
            inner_t = self._parse_inner_array_type(t)
            return {"type": "array", "items": self._py_type_to_swagger(inner_t)}
        # TODO: if SwaggerType.is_swagger_object_type(t):
        if t in (dict, dict):
            raise NotImplementedError("swagger type 'object' is not implemented yet in request schema :(")  # TODO
        if issubclass(t, Enum):
            return {"type": "string", "enum": t.values(), "example": next(e for e in t).value}
        if t in self._PY_TYPE_TO_SWAGGER:
            return self._PY_TYPE_TO_SWAGGER[t]
        raise TypeError(f"{t} type is not supported in request schema")

    def _get_default_value(self) -> tp.Any:
        if self.field.default is not dataclasses.MISSING:
            if isinstance(self.field.default, Enum):
                return self.field.default.value
            return self.field.default
        if self.field.default_factory is not dataclasses.MISSING:
            default = self.field.default_factory()
            if SwaggerType.is_swagger_array_type(self.field.type):
                default = SwaggerType.serialize_array(default)
            # TODO: if SwaggerType.is_swagger_object_type(field.type):
            return default
        raise ValueError("optional request_field should specify default or default_factory")

    def _get_example(self) -> tp.Any:
        t = self.field.type
        if self.is_optional(t):
            t = tp.get_args(t)[0]
        if SwaggerType.is_swagger_array_type(t):
            inner_t = self._parse_inner_array_type(t)
            if issubclass(inner_t, Enum):
                return SwaggerType.serialize_array([e.value for e in inner_t])
            return SwaggerType.serialize_array([self._DEFAULT_SWAGGER_EXAMPLES[inner_t]] * 3)
        # TODO: if SwaggerType.is_swagger_object_type(field.type):
        if issubclass(t, Enum):
            return next(e.value for e in t)
        if t in self._PY_TYPE_TO_SWAGGER:
            return self._DEFAULT_SWAGGER_EXAMPLES[t]
        raise TypeError(f"{t} type is not supported in request schema")

    @classmethod
    def _parse_inner_array_type(cls, t: type) -> type:
        inner_t = t.__args__
        if len(inner_t) != 1:
            raise TypeError("multitype swagger 'array' is not supported in request schema")
        inner_t = inner_t[0]
        if SwaggerType.is_swagger_array_type(inner_t):  # or SwaggerType.is_swagger_object_type(inner_t)
            raise TypeError("swagger types 'array' type with nested collections is not supported in request schema")
        return inner_t


def request_schema(request_cls: BaseRequest) -> TDecorator[THandler]:
    """ Adds request schema parsing and swagger. """
    # aiohttp_apispec.request_schema is not flexible enough

    def decorator(handler: THandler) -> THandler:
        parameters = [
            SwaggerType(field).swagger()
            for field in dataclasses.fields(request_cls)
        ]

        @docs(parameters=parameters)
        @functools.wraps(handler)
        async def wrapper(self: web.View) -> web.Response:
            self.request.data = request_cls.parse(self.request)
            return await handler(self)

        return wrapper
    return decorator
