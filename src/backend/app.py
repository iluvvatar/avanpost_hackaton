import logging
import logging.config
from datetime import datetime

import aiohttp_cors
from aiohttp import web
from aiohttp.web_middlewares import normalize_path_middleware
from aiohttp_apispec import validation_middleware

from backend.middlewares import exceptions_handler_middleware
from backend.swagger import setup_aiohttp_apispec
import backend.views as views


logger = logging.getLogger(__name__)


class Application(web.Application):
    def __init__(self) -> None:
        self._configure_logging()

        super().__init__(middlewares=[
            normalize_path_middleware(),
            exceptions_handler_middleware,
            validation_middleware
        ])

        self.create_time = datetime.now().strftime(r"%Y-%m-%dT%H:%M:%SZ")
        self._configure_logging()
        self._setup_routes()
        self._setup_swagger()
        self._setup_cors()

    def _configure_logging(self) -> None:
        # TODO: is not working
        logging.basicConfig()

    def _setup_swagger(self) -> None:
        logger.debug("Setup swagger")
        setup_aiohttp_apispec(
            app=self,
            title="Panic! At the kernel!",
            version="0.0.1",
            url="/api/docs/swagger.json",
            static_path="/swagger",
            swagger_path="/api/docs",
        )

    def _setup_cors(self) -> None:
        logger.debug("Setup CORS")
        cors = aiohttp_cors.setup(
            self, defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                    allow_methods=["POST", "PUT"],
                ),
            },
        )
        for route in list(self.router.routes()):
            cors.add(route)

    def _setup_routes(self) -> None:
        self.router.add_view(r"/api/v1/ping", views.PingView)
        self.router.add_view(r"/api/v1/versions", views.VersionsView)
        self.router.add_view(r"/api/v1/progress/learn", views.LearnProgressView)
        self.router.add_view(r"/api/v1/progress/download", views.DownloadProgressView)
        self.router.add_view(r"/api/v1/predict", views.PredictImageView)
        self.router.add_view(r"/api/v1/test", views.TestModelView)
