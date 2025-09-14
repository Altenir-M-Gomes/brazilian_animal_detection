from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.usuario import UsuarioModel
from typing import Optional
from typing import Optional, Dict, Any


class UserRepository:

    @staticmethod
    async def findById(db: AsyncSession, id: int):
        result = await db.execute(select(UsuarioModel).where(UsuarioModel.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, user: UsuarioModel):
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
        
    @staticmethod
    async def findBy(db: AsyncSession, **filters) -> Optional[UsuarioModel]:
        query = select(UsuarioModel)
        for attr, value in filters.items():
            query = query.where(getattr(UsuarioModel, attr) == value)

        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update(db: AsyncSession, id: int, data: Dict[str, Any]) -> Optional[UsuarioModel]:
        user = await UserRepository.findById(db=db, id=id)
        
        for key, value in data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)

        await db.commit()
        await db.refresh(user)
        return user
