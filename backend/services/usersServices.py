from typing import Optional
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from configs.database import Session
from models.usuario import UsuarioModel
from ultils.dbSession import getSession
from repository.userRepository import UserRepository
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from configs.envVariables import settings
from schemas.tokenSchemas import TokenPayload

security = HTTPBearer()


async def getCurrentUser(
    db: AsyncSession = Depends(getSession),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UsuarioModel:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível autenticar a credencial",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )

        userId: str = payload.get("sub")
        if userId is None:
            raise credential_exception

    except JWTError:
        raise credential_exception

    # garante que chama o repositório da forma assíncrona
    user: Optional[UsuarioModel] = await UserRepository.findById(
        db=db, id=int(userId)
    )

    if user is None:
        raise credential_exception

    return user
