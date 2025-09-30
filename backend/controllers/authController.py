from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.tokenSchemas import TokenSchema
from schemas.userSchemas import LoginSchema
from services.usersServices import getSession
from services.authServices import AuthService
from ultils.wrapperExecption import wrap_exception  # import do wrapper

class AuthController:

    router = APIRouter()

    @router.post(
        "/login",
        summary="Login de usuário",
        tags=["Autenticação"],
        response_model=TokenSchema
    )
    @wrap_exception
    async def login(body: LoginSchema, db: AsyncSession = Depends(getSession)):
        usuario = await AuthService.authenticateUser(email=body.email, senha=body.senha, db=db)
        return {
            "access_token": AuthService.createAccessToken(sub=usuario.id),
            "token_type": "bearer"
        }
