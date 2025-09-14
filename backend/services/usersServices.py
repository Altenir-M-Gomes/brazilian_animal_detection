from typing import Optional
from fastapi import Depends, status
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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
from datetime import datetime, timedelta
from .authServices import AuthService
from typing import Tuple
from schemas.userSchemas import UsuarioUpdateSchema


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



    async def sendConfirmationEmail(emailTo: str, nome: str, id: str):
        
        
        expire = datetime.utcnow() + timedelta(hours=1)
        payload = {
            "sub": str(id),
            "exp": expire
        }

        token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

        confirmation_link = f"{settings.BASE_URL}/confirm?token={token}"

        message = MessageSchema(
            subject="Confirme seu cadastro",
            recipients=[emailTo],
            body=f"""
            <html>
                <body>
                    <p>Olá {nome},</p>
                    <p>Confirme seu email clicando <a href="{confirmation_link}">aqui</a>.</p>
                    <p>Este link expira em 1 hora.</p>
                </body>
            </html>
            """,
            subtype="html" 
        )

        await mail.send_message(message)



    async def verifyAccount(token: str, db: AsyncSession) -> Tuple[UsuarioModel, str]:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )

        userId: str = payload.get("sub")

        if userId is None:
            raise APIError(errors=[{"message": "Token inválido"}], code=404)

        user: Optional[UsuarioModel] = await UserRepository.findById(db=db, id=int(userId))
        if user is None:
            raise APIError(errors=[{"message": "Usuário não encontrado"}], code=404)

        userUpdated: Optional[UsuarioModel] = await UserRepository.update(db=db, id=int(userId),  data={"ativo": True})
        token = AuthService.createAccessToken(sub=userUpdated.id)
        return userUpdated, token


    async def sendConfirmationResetPasswordEmail(emailTo: str, db: AsyncSession):

        exitUser: Optional[UsuarioModel] = await UserRepository.findBy(db=db, email=emailTo)

        if exitUser is None:
            raise APIError(errors=[{"message": "Email invalido porfavor tente outro!"}], code=404)
                
        expire = datetime.utcnow() + timedelta(hours=1)
        payload = {
            "sub": str(exitUser.id),
            "exp": expire
        }

        token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

        confirmation_link = f"{settings.BASE_URL}/reset-password?token={token}"

        message = MessageSchema(
            subject="Confirme seu cadastro",
            recipients=[emailTo],
            body=f"""
            <html>
                <body>
                    <p>Olá {exitUser.nome},</p>
                    <p>Porfavor click <a href="{confirmation_link}">aqui</a> para redefinir sua senha.</p>
                    <p>Este link expira em 1 hora.</p>
                </body>
            </html>
            """,
            subtype="html" 
        )

        await mail.send_message(message)


    async def defineNewPassword(token: str, newPassword: str, db: AsyncSession) -> Tuple[UsuarioModel, str]:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )

        userId: str = payload.get("sub")
        
        if userId is None:
            raise APIError(errors=[{"message": "Token inválido"}], code=404)

        user: Optional[UsuarioModel] = await UserRepository.findById(db=db, id=int(userId))

        if user is None:
            raise APIError(errors=[{"message": "Usuário não encontrado"}], code=404)

        userUpdated: Optional[UsuarioModel] = await UserRepository.update(db=db, id=int(userId),  data={"senha": createHashPassword(newPassword),})
        token = AuthService.createAccessToken(sub=userUpdated.id)
        return userUpdated, token
    
    @staticmethod
    async def updateUser(user: UsuarioUpdateSchema, db: AsyncSession) -> UsuarioModel:
        
        existingUser: Optional[UsuarioModel] = await UserRepository.findById(db=db, id=user.id)

        if existingUser is None:
            raise APIError(errors=[{"message": "Usuário não encontrado"}], code=404)

        data = {}
        if user.nome is not None:
            data["nome"] = user.nome
        if user.sobrenome is not None:
            data["sobrenome"] = user.sobrenome
        if user.email is not None:
            data["email"] = user.email
        if user.senha is not None:
            data["senha"] = createHashPassword(user.senha)

        updatedUser: Optional[UsuarioModel] = await UserRepository.update(
            db=db,
            id=existingUser.id,
            data=data
        )

        return updatedUser


