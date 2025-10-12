import asyncio
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt
from faker import Faker
from models.usuario import UsuarioModel
from configs.database import engine
from ultils.dbSession import getSession

fake = Faker()

async def seedUsuario() -> None:
    print("Inserindo usuário seed no banco de dados...")

    async for db in getSession():
        async with db.begin():
            try:
                usuario = UsuarioModel(
                    nome="Altenir Modesto Gomes",
                email="altenirgomes@gmail.com",
                senha=bcrypt.hash("senha123"),
                ativo=True
            )
                db.add(usuario)  
                await db.commit()  
                print("Usuário seed criado com sucesso!")
            except IntegrityError:
                await db.rollback()
                print("Usuário já existe, rollback realizado.")

if __name__ == "__main__":
    asyncio.run(seedUsuario())