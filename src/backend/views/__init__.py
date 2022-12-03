import os
import logging

from aiohttp import web
from aiohttp_apispec import docs
from aiohttp_cors import CorsViewMixin

import backend.requests as requests
import backend.responses as responses
from backend.subprocesses import (
    Process,
    download_image,
    predict_single,
    download_dataset,
    predict,
    download_dataset_for_new_class,
    retrain
)

logger = logging.getLogger(__name__)
versions = ['orig']


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
        meta = {}
        return web.json_response(dict(data=versions, meta=meta))


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
        umid = 'umid'
        class_name = 'snowboard'

        def on_trained():
            global versions
            versions.append(Process['RETRAIN'].result['umid'])

        def on_downloaded():
            retrain(umid, class_name, callback=on_trained, blocking=False)

        download_dataset_for_new_class(
                class_name, callback=on_downloaded, blocking=False)

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
        umid = 'm666'
        dataset_url = 'www.example.com'
        def on_predicted():
            global logger
            logger.warn(Process['PREDICT'].result)

        def on_downloaded():
            global logger
            logger.warn(Process['DOWNLOAD_DATASET'].result)
            dataset = Process['DOWNLOAD_DATASET'].result['path']
            predict(umid, dataset, callback=on_predicted, blocking=False)

        download_dataset(dataset_url, callback=on_downloaded, blocking=False)
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
        data = {"img1": ["cat"], "img2": [], "img3": ["cat", "dog"]}
        meta = {"status": responses.EProgressStatus.COMPLETED.value, "percentile": 100}
        return web.json_response(dict(data=data, meta=meta))
