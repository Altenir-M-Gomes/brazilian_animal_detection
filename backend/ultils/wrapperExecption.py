# wrap_exception.py
import functools
import time
from ultils.response import send_error
from ultils.customError import APIError
from ultils.response import send_response

def wrap_exception(fn):
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await fn(*args, **kwargs)
            if result is None:
                return send_response(data=[])
            return result
        except APIError as e:
            return send_error(code=e.code, errors=e.errors)
        except Exception as e:
            # Erro desconhecido
            print(f"Erro inesperado: {e}")
            return send_error(code=500, errors=str(e))
        finally:
            if True: 
                print(f"Tempo de execução {fn.__name__}: {int((time.time() - start_time)*1000)}ms")
    return wrapper
