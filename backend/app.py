from fastapi import APIRouter
from controllers import usuario
from controllers import auth
from controllers import predict

api_router = APIRouter()

api_router.include_router(
    usuario.router, prefix='/users', tags=['Usuário'])
api_router.include_router(
    auth.router, prefix='/auth', tags=['Autenticação'])
api_router.include_router(
    predict.router, prefix='/predict', tags=['Previsão'])
