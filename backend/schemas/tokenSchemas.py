from datetime import datetime
from pydantic import BaseModel
from .userSchemas import UsuarioSchema
class TokenPayload(BaseModel):
    type: str             
    exp: datetime         
    iat: datetime          
    sub: str


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

class TokenVerifySchema(BaseModel):
    token: str

    class Config:
        json_schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            }
        } 

class TokenVerifedSchema(BaseModel):
    user: UsuarioSchema
    access_token: str
    token_type: str
    class Config:
        json_schema_extra = {
            "example": {
                "user":{
                    "id": 1,
                    "nome": "Altenir",
                    "sobrenome": "Modesto Gomes",
                    "email": "altenirgomesmodesto@gmail.com",
                    "ativo": False
                },
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bear"
            }
        } 

