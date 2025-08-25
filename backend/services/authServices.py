from pytz import timezone
from typing import Optional
from datetime import datetime, timedelta
from pydantic import EmailStr
from sqlalchemy.future import select 
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt 
from models.usuario import UsuarioModel
from configs.envVariables import settings
from ultils.security import verifyPassWord
from repository.userRepository import UserRepository

async def auth(email: EmailStr, senha: str, db: AsyncSession) -> Optional[UsuarioModel]:
    user: Optional[UsuarioModel] = await UserRepository.findBy(
        db=db, email=email
    )

    if not user:
        return None

    if not verifyPassWord(senha, user.senha):
        return None

    return user


def _createToken(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:

    payload = {}
    
    zone = timezone('America/Sao_Paulo')
    expira = datetime.now(tz=zone) + tempo_vida

    payload["type"] = tipo_token
    payload["exp"] = expira
    payload["iat"] = datetime.now(tz=zone)
    payload["sub"] = str(sub)
    
    
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def createAcessToken(sub: str) -> str:

    return _createToken(
        tipo_token='acess_token',
        tempo_vida=timedelta(minutes=settings.ACESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )

