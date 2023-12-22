class BaseResponse:

    def __init__(self, status_code: 200, message: str) -> None:
        self.status_code = status_code
        self.message = message

    def toJson(self):
        return {
            "status": self.status_code,
            "message": self.message
        }
