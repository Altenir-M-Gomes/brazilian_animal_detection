from sqlalchemy import Integer, String, Column, Boolean
from configs.envVariables import settings


class UsuarioModel(settings.DBBaseModel):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256), nullable=False)         # no schema é obrigatório
    sobrenome = Column(String(256), nullable=False)    # no schema é obrigatório
    email = Column(String(256), index=True, nullable=False, unique=True)
    senha = Column(String(256), nullable=False)
    ativo = Column(Boolean, default=False, nullable=False)  # corresponde ao schema
