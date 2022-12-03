import typing as tp
import os


class UnconfiguredEnvironment(Exception):
    pass


def get_env(name: str, default: tp.Any = None, *, required: bool = False) -> str:
    env = os.getenv(name, default)
    if required and env is None:
        raise UnconfiguredEnvironment(f"Environment variable {name} is required.")
    return env


STORAGE_PATH = get_env("STORAGE_PATH", "/storage/data")
ORIG_STORAGE_PATH = get_env(STORAGE_PATH, "orig")
GOOGLE_API_KEY = get_env("GOOGLE_API_KEY", required=False)
MOCKED_DATA_PATH = os.path.join(STORAGE_PATH, "mocked_image_search_response.json")
