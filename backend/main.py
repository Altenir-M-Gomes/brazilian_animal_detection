from fastapi import FastAPI
from configs.envVariables import settings
from app import api_router
from fastapi import FastAPI

app = FastAPI(
    title="Brazilian Animal Detection API",
    description="""
API para detecção de animais brasileiros.  
Inclui endpoints para autenticação, usuários e análise de dados.  
""",
    version="1.0.0",
    contact={
        "name": "Seu Nome",
        "email": "seuemail@exemplo.com",
    },
    license_info={
        "name": "MIT License",
    },
)

app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                log_level='info', reload=True)


"""
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjUyNDQyMTE4LCJpYXQiOjE2NTE4MzczMTgsInN1YiI6IjIifQ.5yeW2y_M3eAYrv-369FLsTTkjAFQn6W_eUR19Ivz_YA
Tipo: bearer

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjUyNDQzNDk1LCJpYXQiOjE2NTE4Mzg2OTUsInN1YiI6IjMifQ.jTq0xkcILa7kgrtMJhcew6OIwXODEjX24CzCToY7bbU
"""
