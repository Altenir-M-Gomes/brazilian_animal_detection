from fastapi import APIRouter
from controllers import userController
from controllers import authController
from controllers import predictController

api_router = APIRouter()

api_router.include_router(
    userController.router, prefix='/users', tags=['Usuário'])
api_router.include_router(
    authController.router, prefix='/auth', tags=['Autenticação'])
api_router.include_router(
    predictController.router, prefix='/predict', tags=['Previsão'])
