import logging

from aiohttp import web
from aiohttp_apispec import docs
from aiohttp_cors import CorsViewMixin

import backend.requests as requests
import backend.responses as responses

logger = logging.getLogger(__name__)


class PingView(web.View, CorsViewMixin):
    @docs(
        summary="Возвращает 200 ОК",
        description="ping",
        responses={
            200: {
                "description": "OK",
            },
        },
    )
    async def get(self) -> web.Response:
        return web.json_response()


class VersionsListView(web.View, CorsViewMixin):
    @docs(
        summary="Возвращает список версий модели",
        responses={
            200: {
                "schema": responses.VersionsListResponse.Schema(),
                "description": "Список версий",
            },
            420: {
                "description": "Request error",
            },
        },
    )
    async def get(self) -> web.Response:
        data = ["version1", "version2"]
        meta = {}
        return web.json_response(dict(data=data, meta=meta))


class NewVersionView(web.View, CorsViewMixin):
    @docs(
        summary="Создать новую версию модели (дообучить распознавать новый класс)",
        responses={
            201: {
                "description": "Started",
            },
            420: {
                "description": "Request error",
            },
        },
    )
    @requests.request_schema(requests.NewVersionRequest)
    async def post(self) -> web.Response:
        request_data: requests.NewVersionRequest = self.request.data
        return web.json_response(status=201)


class PredictImageView(web.View, CorsViewMixin):
    @docs(
        summary="Возвращает предсказание для одной картинки",
        responses={
            200: {
                "schema": responses.PredictImageResponse.Schema(),
                "description": "Предсказание",
            },
            420: {
                "description": "Request error",
            },
        },
    )
    @requests.request_schema(requests.PredictImageRequest)
    async def get(self) -> web.Response:
        request_data: requests.PredictImageRequest = self.request.data
        data = {"image_url": "http://localhost", "label": "cat", "probability": 100}
        meta = {}
        return web.json_response(dict(data=data, meta=meta))


class TestModelView(web.View, CorsViewMixin):
    @docs(
        summary="Протестировать модель на тестовом датасете и вернуть метрики",
        responses={
            201: {
                "description": "Started",
            },
            420: {
                "description": "Request error",
            },
        },
    )
    @requests.request_schema(requests.TestModelRequest)
    async def post(self) -> web.Response:
        request_data: requests.TestModelRequest = self.request.data
        return web.json_response(status=201)


class LearnProgressView(web.View, CorsViewMixin):
    @docs(
        summary="Возвращает значение прогресса обучения в процентах",
        responses={
            200: {
                "schema": responses.ProgressResponse.Schema(),
                "description": "Прогресс обучения в процентах",
            },
        },
    )
    async def get(self) -> web.Response:
        data = {}
        meta = {"status": responses.EProgressStatus.RUNNING.value, "percentile": 50}
        return web.json_response(dict(data=data, meta=meta))


class DownloadProgressView(web.View, CorsViewMixin):
    @docs(
        summary="Возвращает значение прогресса скачивания датасета",
        responses={
            200: {
                "schema": responses.ProgressResponse.Schema(),
                "description": "Прогресс скачивания датасета",
            },
        },
    )
    async def get(self) -> web.Response:
        data = {}
        meta = {"status": responses.EProgressStatus.RUNNING.value, "percentile": 50}
        return web.json_response(dict(data=data, meta=meta))


class TestModelProgressView(web.View, CorsViewMixin):
    @docs(
        summary="Прогноз и результат тестирования модели",
        responses={
            200: {
                "schema": responses.TestModelProgressResponse.Schema(),
                "description": "Прогресс и результат тестирования модели",
            },
        },
    )
    async def get(self) -> web.Response:
        data = {"metrics": {"accuracy": 100, "f1": 1}}
        meta = {"status": responses.EProgressStatus.COMPLETED.value, "percentile": 100}
        return web.json_response(dict(data=data, meta=meta))
