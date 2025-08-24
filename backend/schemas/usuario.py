from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class TokenSchema(BaseModel):
    access_token: str
    token_type: str

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class LoginSchema(BaseModel):
    email: EmailStr = Field(..., example="teste@email.com")
    senha: str = Field(..., example="123456")

class UsuarioSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr

    class Config:
        from_attributes  = True

class UsuarioSchemaCreate(UsuarioSchema):
    senha: str

class UsuarioSchemaUp(UsuarioSchema):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
