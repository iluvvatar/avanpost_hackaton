import logging

from aiohttp import web

from backend.app import Application

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    app = Application()
    web.run_app(app, host="0.0.0.0", port=8080, access_log=logger)
