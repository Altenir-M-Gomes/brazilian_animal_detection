from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.usuario import UsuarioModel
from schemas.usuario import UsuarioSchema, UsuarioSchemaCreate, UsuarioSchemaUp,  TokenSchema
from services.users import getSession, getCurrentUser
from services.auth import auth, createAcessToken
from ultils.security import createHashPassword
from schemas.usuario import LoginSchema

router = APIRouter()

@router.post('/login', summary="Login de usuário", tags=["Autenticação"], response_model=TokenSchema)
async def login(
    body: LoginSchema,
    db: AsyncSession = Depends(getSession)
):
    """
    Realiza login de usuário.

    - **email**: Email do usuário
    - **senha**: Senha do usuário
    """
    usuario = await auth(email=body.email, senha=body.senha, db=db)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Dados de acesso incorretos.'
        )

    return {
        "access_token": createAcessToken(sub=usuario.id),
        "token_type": "bearer"
    }
