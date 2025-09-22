from fastapi.responses import JSONResponse
from fastapi import status
from typing import Any, List, Union, Dict

# Padrão de mensagens HTTP
http_messages = {
    200: "OK",
    201: "Created",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    409: "Conflict",
    500: "Internal Server Error",
}

def sendResponse(
    data: Any = None,
    code: int = status.HTTP_200_OK,
    message: str = None,
    errors: List[Dict[str, Any]] = None
) -> JSONResponse:
    """
    Retorna resposta padronizada de sucesso.
    """
    payload = {
        "data": data or [],
        "error": False,
        "code": code,
        "message": message or http_messages.get(code, ""),
        "errors": errors or [],
    }
    return JSONResponse(status_code=code, content=payload)

def sendError(
    code: int = status.HTTP_400_BAD_REQUEST,
    errors: Union[str, Dict[str, Any], List[Dict[str, Any]]] = None
) -> JSONResponse:
    """
    Retorna resposta padronizada de erro.
    Aceita:
      - string -> [{"message": "texto"}]
      - dict -> [{"message": dict["message"], ...}]
      - list de dicts -> [{"message": "msg"}, ...]
    """
    _errors: List[Dict[str, Any]] = []

    if isinstance(errors, str):
        _errors = [{"message": errors}]
    elif isinstance(errors, dict) and "message" in errors:
        _errors = [errors]
    elif isinstance(errors, list):
        _errors = errors
    else:
        _errors = [{"message": "Erro desconhecido"}]

    payload = {
        "data": [],
        "error": True,
        "code": code,
        "message": http_messages.get(code, ""),
        "errors": _errors,
    }

    return JSONResponse(status_code=code, content=payload)
