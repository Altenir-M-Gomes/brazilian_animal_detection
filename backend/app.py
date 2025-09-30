from fastapi import APIRouter
from controllers.userController import UserController
from controllers.authController import AuthController
from controllers import predictController

api_router = APIRouter()

api_router.include_router(
    UserController().router, prefix='/users', tags=['Usuário'])
api_router.include_router(
    AuthController().router, prefix='/auth', tags=['Autenticação'])
api_router.include_router(
    predictController.router, prefix='/predict', tags=['Previsão'])
