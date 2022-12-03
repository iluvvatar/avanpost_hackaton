import logging
import traceback
import typing as tp

from aiohttp import web

from backend.errors import ServiceError

logger = logging.getLogger(__name__)
traceback_logger = logging.getLogger("traceback")

THandler = tp.Callable[[web.Request], tp.Awaitable[web.Response]]


@web.middleware
async def exceptions_handler_middleware(request: web.Request, handler: THandler) -> None:
    try:
        logger.info(f"{request.method} {request.rel_url}")
        return await handler(request)
    except ServiceError as err:
        error = {
            "message": err.msg,
            "error_name": err.name,
            "error_code": err.code,
        }
        logger.info(f"{request.method} {request.rel_url} | error: {error}")
        return web.json_response(error, status=err.code)
    except web.HTTPError as err:
        error = {
            "message": err.text,
            "error_name": err.__class__.__name__,
            "error_code": err.status_code,
        }
        logger.info(f"{request.method} {request.rel_url} | error: {error}")
        return web.json_response(error, status=err.status_code)
    except Exception as err:
        tbk = traceback.format_exc()
        traceback_logger.error(tbk)
        error = {
            "message": tbk,
            "error_name": err.__class__.__name__,
            "error_code": 500,
        }
        return web.json_response(error, status=500)
