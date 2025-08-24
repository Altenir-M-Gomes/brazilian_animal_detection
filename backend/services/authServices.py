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
from fastapi.security import HTTPBearer

bearer_scheme = HTTPBearer()

async def auth(email: EmailStr, senha: str, db: AsyncSession) -> Optional[UsuarioModel]:
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.email == email)
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()

        if not usuario:
            return None

        if not verifyPassWord(senha, usuario.senha):
            return None

        return usuario


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

