from fastapi import HTTPException

class APIError(HTTPException):
    def __init__(self, errors: list = None, code: int = 400):
        message = errors[0]["message"] if errors else f"Erro com código {code}"
        super().__init__(status_code=code, detail=errors or [{"message": message}])
        self.errors = errors
        self.code = code
