from pytz import timezone
from typing import Optional
from datetime import datetime, timedelta
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from ultils.customError import APIError
from models.usuario import UsuarioModel
from configs.envVariables import settings
from ultils.security import verifyPassWord
from repository.userRepository import UserRepository

class AuthService:
    zone = timezone("America/Sao_Paulo")

    @staticmethod
    async def authenticateUser(db: AsyncSession, email: EmailStr, senha: str) -> Optional[UsuarioModel]:
        
        user: Optional[UsuarioModel] = await UserRepository.findBy(db=db, email=email)

        if not user:
            raise APIError(errors=[{"message": "Usuário não encontrado"}], code=404)
        
        elif not verifyPassWord(senha, user.senha):
            raise APIError(errors=[{"message": "Senha incorreta"}], code=400)

        return user

    @classmethod
    def _createToken(cls, tipoToken: str, tempo_vida: timedelta, sub: str) -> str:
        """
        Cria um JWT com tempo de expiração e tipo de token.
        """
        payload = {}
        expira = datetime.now(tz=cls.zone) + tempo_vida

        payload["type"] = tipoToken
        payload["exp"] = expira
        payload["iat"] = datetime.now(tz=cls.zone)
        payload["sub"] = str(sub)

        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

    @classmethod
    def createAccessToken(cls, sub: str) -> str:
        """
        Cria token de acesso com tempo de expiração padrão.
        """
        return cls._createToken(
            tipoToken="access_token",
            tempo_vida=timedelta(minutes=settings.ACESS_TOKEN_EXPIRE_MINUTES),
            sub=sub
        )

   