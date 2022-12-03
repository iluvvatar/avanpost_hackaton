class ServiceError(Exception):
    def __init__(self, msg: str | None = None, code: int = 500) -> None:
        self.msg = msg
        self.code = code
        super().__init__(self.msg)
    
    @property
    def name(self) -> str:
        return self.__class__.__name__


class RequestError(Exception):
    def __init__(self, msg: str | None = None) -> None:
        super().__init__(msg, 422)
