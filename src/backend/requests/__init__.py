import marshmallow as msh

from backend.requests.base import BaseRequest, request_field, Enum, ERequestLocation, request_schema


class NewVersionRequest(BaseRequest):
    model_version: str = request_field(
        location=ERequestLocation.QUERY,
        description="Model version to use for evaluation",
        required=True
    )
    label: str = request_field(
        location=ERequestLocation.QUERY,
        description="Class label",
        required=True
    )


class PredictImageRequest(BaseRequest):
    model_version: str = request_field(
        location=ERequestLocation.QUERY,
        description="Model version to use for evaluation",
        required=True
    )
    image_url: str = request_field.FromMsh(
        msh.fields.Url(),
        location=ERequestLocation.QUERY,
        description="Url to download an image",
        required=True
    )


class TestModelRequest(BaseRequest):
    model_version: str = request_field(
        location=ERequestLocation.QUERY,
        description="Model version to use for evaluation",
        required=True
    )
    data_url: str = request_field.FromMsh(
        msh.fields.Url(),
        location=ERequestLocation.QUERY,
        description=(
            "Url to labeled dataset. "
            "Url should link to archive containing images structured into folders with class label name."
        ),
        required=True
    )
