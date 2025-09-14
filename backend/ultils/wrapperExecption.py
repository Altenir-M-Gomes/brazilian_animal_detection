# wrap_exception.py
import functools
import time
from fastapi.responses import JSONResponse
from ultils.customError import APIError

def wrap_exception(fn):
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            return await fn(*args, **kwargs)
        except APIError as e:
            return JSONResponse(status_code=e.code, content={"errors": e.errors})
        except Exception as e:
            # erro desconhecido
            print(f"Erro inesperado: {e}")
            return JSONResponse(status_code=500, content={"errors": [{"message": str(e)}]})
        finally:
            # medir tempo se quiser
            if True:  # pode colocar DEBUG via env
                print(f"Tempo de execução {fn.__name__}: {int((time.time() - start_time)*1000)}ms")
    return wrapper
