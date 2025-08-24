from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import usuario as User # seu modelo SQLAlchemy
from schemas.usuario import UsuarioSchemaCreate, UsuarioSchemaUp  # Pydantic schemas


class UserRepository:

    @staticmethod
    async def findById(db: AsyncSession, id: int):
        result = await db.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, data: UsuarioSchemaCreate):
        user = User(**data)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def update(db: AsyncSession, id: int, data: UsuarioSchemaUp):
        result = await db.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        if not user:
            return None
        for key, value in data.items():
            setattr(user, key, value)
        await db.commit()
        await db.refresh(user)
        return user
