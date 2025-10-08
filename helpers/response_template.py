class ResponseTemplate:
    def __init__(self, data: dict, status: int, message: str):
        self.data = data
        self.status = status
        self.message = message

    def to_dict(self):
        return {
            "data": self.data,
            "status": self.status,
            "message": self.message,
        }
