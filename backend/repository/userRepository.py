from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import usuario as User # seu modelo SQLAlchemy
from schemas.userSchemas import UsuarioSchemaCreate  # Pydantic schemas


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