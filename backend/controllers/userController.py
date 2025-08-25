
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.usuario import UsuarioModel
from schemas.userSchemas import UsuarioSchema, UsuarioSchemaCreate
from services.usersServices import getSession
from ultils.security import createHashPassword

router = APIRouter()


# POST / Signup
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchema, tags=['Usuário'])
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(getSession)):
    novo_usuario: UsuarioModel = UsuarioModel(nome=usuario.nome, sobrenome=usuario.sobrenome,
                                              email=usuario.email, senha=createHashPassword(usuario.senha))
    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()

            return novo_usuario
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Já existe um usuário com este email cadastrado.')
