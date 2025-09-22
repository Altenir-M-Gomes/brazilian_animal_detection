# wrap_exception.py
import functools
import time
from ultils.response import sendError, sendResponse
from ultils.customError import APIError

def wrap_exception(fn):
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await fn(*args, **kwargs)

            if result is None:
                return sendResponse(data=[])
            return sendResponse(data=result)

        except APIError as e:
            return sendError(code=e.code, errors=e.errors)
        except Exception as e:
            # Erro inesperado
            print(f"Erro inesperado: {e}")
            return sendError(code=500, errors=str(e))
        finally:
            print(f"Tempo de execução {fn.__name__}: {int((time.time() - start_time)*1000)}ms")
    return wrapper
