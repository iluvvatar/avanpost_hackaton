import os
import logging

from aiohttp import web
from aiohttp_apispec import docs
from aiohttp_cors import CorsViewMixin


import backend.requests as requests
import backend.responses as responses
from backend.subprocesses import Process, download_image, predict_single

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


class VersionsView(web.View, CorsViewMixin):
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

    @docs(
        summary="Создать новую версию модели (дообучить распознавать новый класс)",
        responses={
            201: {
                "description": "OK",
            },
            420: {
                "description": "Request error",
            },
        },
    )
    @requests.request_schema(requests.CreateVersionRequest)
    async def post(self) -> web.Response:
        request_data: requests.CreateVersionRequest = self.request.data
        data = ["version1", "version2"]
        meta = {}
        return web.json_response(dict(data=data, meta=meta))


class LearnProgressView(web.View, CorsViewMixin):
    @docs(
        summary="Возвращает значение прогресса обучения в процентах",
        responses={
            200: {
                "schema": responses.LearnProgressResponse.Schema(),
                "description": "Прогресс обучения в процентах",
            },
            420: {
                "description": "Request error",
            },
        },
    )
    async def get(self) -> web.Response:
        data = 50
        meta = {}
        return web.json_response(dict(data=data, meta=meta))


class DownloadProgressView(web.View, CorsViewMixin):
    @docs(
        summary="Возвращает значение прогресса скачивания датасета",
        responses={
            200: {
                "schema": responses.DownloadProgressResponse.Schema(),
                "description": "Прогресс скачивания датасета",
            },
            420: {
                "description": "Request error",
            },
        },
    )
    async def get(self) -> web.Response:
        data = 50
        meta = {}
        return web.json_response(dict(data=data, meta=meta))


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
        umid = 'umid'
        image_url = os.getenv('RANDOM_IMAGE_FROM_INTERNET')
        prediction = None

        def on_downloaded():
            predict_single(umid, callback=None, blocking=True)
            nonlocal prediction
            prediction = Process['PREDICT_SINGLE'].result

        download_image(image_url, callback=on_downloaded, blocking=True)
        data = {
            "image_url": image_url,
            "label": prediction["label"],
            "probability": prediction["probability"]
        }
        meta = {}
        return web.json_response(dict(data=data, meta=meta))


class TestModelView(web.View, CorsViewMixin):
    @docs(
        summary="Протестировать модель на тестовом датасете и вернуть метрики",
        responses={
            200: {
                "schema": responses.TestModelResponse.Schema(),
                "description": "Предсказание",
            },
            420: {
                "description": "Request error",
            },
        },
    )
    @requests.request_schema(requests.TestModelRequest)
    async def get(self) -> web.Response:
        data = {"metrics": {"accuracy": 100, "f1": 1}}
        meta = {}
        return web.json_response(dict(data=data, meta=meta))
