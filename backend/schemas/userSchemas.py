from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class LoginSchema(BaseModel):
    email: EmailStr = Field(..., example="altenirgomes@gmail.com")
    senha: str = Field(..., example="12345")

class UsuarioSchema(BaseModel):
    id: Optional[int] = Field(..., example="1")
    nome: str = Field(..., example="Altenir")
    sobrenome: str = Field(..., example="Modesto Gomes")
    email: EmailStr = Field(..., example="altenirgomes@gmail.com")

    class Config:
        from_attributes  = True

class UsuarioSchemaCreate(UsuarioSchema):
    senha: str = Field(..., example="12345")
