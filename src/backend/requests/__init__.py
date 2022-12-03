from backend.requests.base import BaseRequest, request_field, Enum, ERequestLocation, request_schema


class HelloRequest(BaseRequest):
    message: str = request_field(
        location=ERequestLocation.QUERY,
        description="message",
        default="123"
    )
