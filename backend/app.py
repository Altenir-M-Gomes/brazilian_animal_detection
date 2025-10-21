from fastapi import APIRouter
from controllers.userController import UserController
from controllers.authController import AuthController
from controllers.predictController import PredictionController

api_router = APIRouter()

api_router.include_router(
    UserController().router, prefix='/users', tags=['Usuário'])
api_router.include_router(
    AuthController().router, prefix='/auth', tags=['Autenticação'])
api_router.include_router(
    PredictionController.router, prefix='/predict', tags=['Previsão'])
