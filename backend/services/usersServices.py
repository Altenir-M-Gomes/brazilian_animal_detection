from typing import Optional
from fastapi import Depends, status
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from ultils.customError import APIError
from ultils.dbSession import getSession
from repository.userRepository import UserRepository
from configs.envVariables import settings
from models.usuario import UsuarioModel
from ultils.wrapperExecption import wrap_exception
from schemas.userSchemas import UsuarioSchemaCreate 
from ultils.security import createHashPassword
from fastapi_mail import MessageSchema
from configs.emailConfig import mail

class UserService:

    security = HTTPBearer()

    # Situação especial que tem ultilizar o wrap pois ele é uma sessão
    @staticmethod
    @wrap_exception
    async def getCurrentUser(
        db: AsyncSession = Depends(getSession),
        credentials: HTTPAuthorizationCredentials = Depends(security),
    ) -> UsuarioModel:
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )

        userId: str = payload.get("sub")
        if userId is None:
            raise APIError(errors=[{"message": "Token inválido"}], code=401)

        user: Optional[UsuarioModel] = await UserRepository.findById(db=db, id=int(userId))
        if user is None:
            raise APIError(errors=[{"message": "Usuário não encontrado"}], code=401)

        return user
    
    @staticmethod
    async def createUser(user: UsuarioSchemaCreate, db: AsyncSession) -> UsuarioModel:
        
        exitUser: Optional[UsuarioModel] = await UserRepository.findBy(db=db, email=user.email)
        if exitUser:
            raise APIError(
                errors=[{"message": "Já existe um usuário com este email cadastrado."}],
                code=status.HTTP_406_NOT_ACCEPTABLE,
            )
        
        newUser = UsuarioModel(
            nome=user.nome,
            sobrenome=user.sobrenome,
            email=user.email,
            senha=createHashPassword(user.senha),
        )

        return await UserRepository.create(db=db, user=newUser)

    async def sendConfirmationEmail(email_to: str, nome: str, token: str):
        # usa a BASE_URL do settings
        confirmation_link = f"{settings.BASE_URL}/api/v1/users/confirm?token={token}"
    
        message = MessageSchema(
            subject="Confirme seu cadastro",
            recipients=[email_to],
            body=f"""
            <html>
                <body>
                    <p>Olá {nome},</p>
                    <p>Confirme seu email clicando <a href="{confirmation_link}">aqui</a>.</p>
                </body>
            </html>
            """,
            subtype="html" 
        )
    
        await mail.send_message(message)
