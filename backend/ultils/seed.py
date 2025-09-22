import asyncio
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt
from faker import Faker
from models.usuario import UsuarioModel
from configs.database import engine

fake = Faker()

async def seedUsuario() -> None:
    print("Inserindo usuário seed no banco de dados...")

    async with engine.begin() as conn:

        try:
            usuario = UsuarioModel(
                nome="Altenir",
                sobrenome="Modesto Gomes",
                email="altenirgomes@gmail.com",
                senha=bcrypt.hash("senha123"),
                ativo=True
            )
            conn.add(usuario)  
            await conn.commit()  
            print("Usuário seed criado com sucesso!")
        except IntegrityError:
            await conn.rollback()
            print("Usuário já existe, rollback realizado.")

if __name__ == "__main__":
    asyncio.run(seedUsuario())