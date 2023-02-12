from fastapi.exceptions import HTTPException
from typing import Any, Optional, Dict


class ValidationException(HTTPException):
    def __init__(self, field: str, error: str) -> None:
        super().__init__(status_code=403, detail={"field": field, "error": error})

class NoContentException(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=204, detail={"error": detail})