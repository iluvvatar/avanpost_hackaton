import typing as tp

from aiohttp import web
from aiohttp_apispec import AiohttpApiSpec


class Swagger:
    swagger_dict: dict[str, dict] = None
    spec: AiohttpApiSpec = None


def get_swagger_dict() -> dict:
    return Swagger.swagger_dict


def setup_aiohttp_apispec(
    app: web.Application,
    *,
    title: str = "API documentation",
    version: str = "0.0.1",
    url: str = "/api/docs/swagger.json",
    request_data_name: str = "data",
    swagger_path: str = None,
    static_path: str = "/static/swagger",
    error_callback=None,
    in_place: bool = False,
    prefix: str = "",
    **kwargs: tp.Any,
) -> None:
    spec = AiohttpApiSpec(
        url=url,
        app=app,
        request_data_name=request_data_name,
        title=title,
        version=version,
        swagger_path=swagger_path,
        static_path=static_path,
        error_callback=error_callback,
        in_place=in_place,
        prefix=prefix,
        **kwargs,
    )
    Swagger.spec = spec
    Swagger.swagger_dict = spec.swagger_dict()
