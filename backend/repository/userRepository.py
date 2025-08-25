from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import usuario as User # seu modelo SQLAlchemy
from schemas.userSchemas import UsuarioSchemaCreate  # Pydantic schemas
from models.usuario import UsuarioModel
from typing import List


class UserRepository:

    @staticmethod
    async def findById(db: AsyncSession, id: int):
        result = await db.execute(select(UsuarioModel).where(UsuarioModel.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, data: UsuarioSchemaCreate):
        user = User(**data)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
        
    @staticmethod
    async def findBy(db: AsyncSession, **filters) -> list[UsuarioModel]:
        query = select(UsuarioModel)
        for attr, value in filters.items():
            query = query.where(getattr(UsuarioModel, attr) == value)

        result = await db.execute(query)
        return result.scalar_one_or_none()
