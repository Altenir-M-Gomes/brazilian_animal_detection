
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.userSchemas import UsuarioSchema, UsuarioSchemaCreate
from services.usersServices import getSession
from ultils.wrapperExecption import wrap_exception
from services.usersServices import UserService
from models.usuario import UsuarioModel

class UserController:
    router = APIRouter()


    @router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchema, tags=['Usuário'])
    @wrap_exception
    async def createUser(user: UsuarioSchemaCreate, db: AsyncSession = Depends(getSession)):
        newUser: UsuarioModel = await UserService.createUser(user=user, db=db)
        
        await UserService.sendConfirmationEmail(email_to = newUser.email, nome = newUser.nome, token = '')
        
        return newUser
         