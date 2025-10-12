
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.userSchemas import UsuarioSchema, UsuarioSchemaCreate
from services.usersServices import getSession
from ultils.wrapperExecption import wrap_exception
from services.usersServices import UserService
from models.usuario import UsuarioModel
from schemas.tokenSchemas import TokenVerifedSchema
from schemas.tokenSchemas import TokenVerifySchema
from schemas.userSchemas import ResetPasswordResponseSchema
from schemas.userSchemas import ResetPasswordEmailSchema
from schemas.userSchemas import UsuarioUpdateSchema
from typing import Tuple

class UserController:
    router = APIRouter()


    @router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchema, tags=['Usuário'])
    @wrap_exception
    async def createUser(user: UsuarioSchemaCreate, db: AsyncSession = Depends(getSession)):
        newUser: UsuarioModel = await UserService.createUser(user=user, db=db)
        
        await UserService.sendConfirmationEmail(emailTo = newUser.email, nome = newUser.nome, id=int(newUser.id))
        
        return {
            "id": newUser.id,
            "nome": newUser.nome,
            "email": newUser.email,
            "ativo": newUser.ativo
        }
        
    
    @router.post('/verify-acount', status_code=status.HTTP_201_CREATED, response_model=TokenVerifedSchema, tags=['Usuário'])
    @wrap_exception
    async def verifyAcount(body: TokenVerifySchema, db: AsyncSession = Depends(getSession)):
        
        authToken: Tuple[UsuarioModel, str] = await UserService.verifyAccount(token=body.token, db=db)
        
        return {
            "user": authToken[0],
            "access_token": authToken[1],
            "token_type": "bearer"

        }
    
    @router.post('/reset-password', status_code=status.HTTP_201_CREATED, response_model=ResetPasswordResponseSchema, tags=['Usuário'])
    @wrap_exception
    async def resetPassword(email: ResetPasswordEmailSchema, db: AsyncSession = Depends(getSession)):
        
        await UserService.sendConfirmationResetPasswordEmail(emailTo=email, db=db)
        
        return {
            "mensagem": 'Foi enviado o email para alterar a senha!'
        }

    @router.post('/define-password', status_code=status.HTTP_201_CREATED, response_model=TokenVerifedSchema, tags=['Usuário'])
    @wrap_exception
    async def definePassword(body: TokenVerifySchema, db: AsyncSession = Depends(getSession)):
        
        authToken: Tuple[UsuarioModel, str] = await UserService.defineNewPassword(token=body.token, db=db)
        
        return {
            "user": authToken[0],
            "access_token": authToken[1],
            "token_type": "bearer"

        }

    @router.patch('/user', status_code=status.HTTP_201_CREATED, response_model=UsuarioUpdateSchema, tags=['Usuário'])
    @wrap_exception
    async def updateUser(body: UsuarioUpdateSchema, db: AsyncSession = Depends(getSession)):
        
        authToken: Tuple[UsuarioModel, str] = await UserService.defineNewPassword(token=body.token, db=db)
        
        return {
            "user": authToken[0],
            "access_token": authToken[1],
            "token_type": "bearer"
        }



         