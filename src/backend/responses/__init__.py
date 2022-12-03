import typing as tp

from backend.core import DataClass


class VersionsListResponse(DataClass):
    data: list[str]
    meta: dict[str, tp.Any]


class LearnProgressResponse(DataClass):
    data: int
    meta: dict[str, tp.Any]


class DownloadProgressResponse(DataClass):
    data: int
    meta: dict[str, tp.Any]


class PredictImageResponse(DataClass):

    class LearnProgressData(DataClass):
        label: str
        probability: float

    data: LearnProgressData
    meta: dict[str, tp.Any]


class TestModelResponse(DataClass):

    class TestModelData(DataClass):
        metrics: dict[str, float]

    data: TestModelData
    meta: dict[str, tp.Any]
