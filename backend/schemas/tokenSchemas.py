from datetime import datetime
from pydantic import BaseModel

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
