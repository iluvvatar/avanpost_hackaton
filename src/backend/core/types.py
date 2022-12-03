import typing as tp
from aiohttp import web


THandler = tp.Callable[[web.View], tp.Awaitable[web.Response]]
TJsonSerializable = tp.Union[
    None,
    str,
    int,
    float,
    bool,
    dict[tp.Hashable, "TJsonSerializable"],
    list["TJsonSerializable"]
]
RT = tp.TypeVar("RT")
TDecorator = tp.Callable[[RT], RT]
