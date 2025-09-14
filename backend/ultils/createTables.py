from configs.envVariables import settings
from configs.database import engine
from models.usuario import UsuarioModel  # importe todos os modelos aqui
import asyncio

async def createTables() -> None:
    print('Criando as tabelas no banco de dados')

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)

    print('Tabelas criadas com sucesso...')

if __name__ == '__main__':
    asyncio.run(createTables())
