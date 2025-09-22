import asyncio
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt
from faker import Faker
from models.usuario import UsuarioModel
from services.usersServices import getSession  

fake = Faker()

async def seed_usuarios():
    async with getSession() as db:
        async with db.begin():
            for _ in range(10):  # cria 10 usuários fake
                nome = 'Altenir'
                sobrenome = fake.last_name()
                email = "altenirgomes@gmail.com"
                senha = bcrypt.hash("senha123")  # senha padrão para todos
                
                usuario = UsuarioModel(
                    nome=nome,
                    sobrenome=sobrenome,
                    email=email,
                    senha=senha,
                    ativo=True
                )
                db.add(usuario)
            try:
                await db.commit()
                print("Seed finalizado com sucesso!")
            except IntegrityError:
                await db.rollback()
                print("Algum usuário já existia, rollback realizado.")

if __name__ == "__main__":
    asyncio.run(seed_usuarios())
