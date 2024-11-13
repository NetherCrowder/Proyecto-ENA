class Error:
    def __init__(self, code, message):
        self.code = code
        self.message = message

    @staticmethod
    def unauthorized():
        return Error(401, "Unauthorized")

    @staticmethod
    def not_found(message: str = "Not Found"):
        return Error(404, "Not Found")

    @staticmethod
    def validation(message: str = "Bad Request"):
        return Error(400, message)

    @staticmethod
    def unexpected():
        return Error(500, "Internal Server Error")

    @staticmethod
    def not_implemented():
        return Error(501, "Not Implemented")

    @staticmethod
    def from_exception(exception: Exception, code: int = 424):
        return Error(code, str(exception))

    @staticmethod
    def custom(code, message):
        return Error(code, message)

    def __eq__(self, other):
        return isinstance(other, Error) and self.code == other.code and self.message == other.message
