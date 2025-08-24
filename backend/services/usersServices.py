from typing import Optional
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.future import select
from configs.database import Session
from models.usuario import UsuarioModel
from ultils.dbSession import getSession
from repository.userRepository import UserRepository
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from configs.envVariables import settings
from schemas.userSchemas import TokenSchema


security = HTTPBearer()


async def getCurrentUser(db: Session = Depends(getSession), credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UsuarioModel:
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Não foi possível autenticar a credencial',
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            credentials,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )

        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data: TokenSchema = TokenSchema(username=username)
    except JWTError:
        raise credential_exception

    user: Optional[object] = UserRepository.findById(db=db, id=int(token_data.username))

    if user is None:
        raise credential_exception

    return user