import typing as tp

from backend.core import DataClass, Enum


class EProgressStatus(Enum):
    RUNNING = "running"
    COMPLETED = "completed"


class EmptyDataResponse(DataClass):
    data: dict[str, tp.Any]


class EmptyMetaResponse(DataClass):
    meta: dict[str, tp.Any]


class VersionsListResponse(EmptyMetaResponse):
    data: list[str]


class PredictImageResponse(EmptyMetaResponse):

    class PredictImageData(DataClass):
        image_url: str
        label: str
        probability: float

    data: PredictImageData


class ProgressResponse(EmptyDataResponse):

    class ProgressMeta(DataClass):
        status: EProgressStatus
        percentile: int
    
    meta: ProgressMeta


class TestModelProgressResponse(ProgressResponse):
    data: dict[str, list[str]]
