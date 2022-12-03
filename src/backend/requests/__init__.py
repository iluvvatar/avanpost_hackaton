import marshmallow as msh

from backend.requests.base import BaseRequest, request_field, Enum, ERequestLocation, request_schema


class CreateVersionRequest(BaseRequest):
    label: str = request_field(
        location=ERequestLocation.QUERY,
        description="Class label",
        required=True
    )
    data_url: str = request_field.FromMsh(
        msh.fields.Url(),
        location=ERequestLocation.QUERY,
        description="Url to archive with images of new class",
        required=True
    )


class PredictImageRequest(BaseRequest):
    image_url: str = request_field.FromMsh(
        msh.fields.Url(),
        location=ERequestLocation.QUERY,
        description="Url to download an image",
        required=True
    )


class TestModelRequest(BaseRequest):
    data_url: str = request_field.FromMsh(
        msh.fields.Url(),
        location=ERequestLocation.QUERY,
        description=(
            "Url to labeled dataset. "
            "Url should link to archive containing images structured into folders with class label name."
        ),
        required=True
    )
