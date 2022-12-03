import logging

from aiohttp import web
from aiohttp_apispec import docs
from aiohttp_cors import CorsViewMixin


from backend.requests import HelloRequest, request_schema

logger = logging.getLogger(__name__)


class HellloView(web.View, CorsViewMixin):
    @docs(
        summary="Hello",
        description="hello",
        responses={
            200: {
                "description": "hello",
            },
            420: {
                "description": "err",
            },
        },
    )
    @request_schema(HelloRequest)
    async def get(self) -> web.Response:
        data = self.request.data
        print(data)
        return web.json_response({})
