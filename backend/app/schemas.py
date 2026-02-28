"""
Schemas de Pydantic
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Usuario
class UserBase(BaseModel):
    email: EmailStr
    nombre: str

class UserCreate(UserBase):
    password: str
    rol: str = "Usuario"
    organizacion_id: Optional[int] = None

class UserResponse(UserBase):
    id: int
    rol: str
    activo: bool
    organizacion_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Token
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    email: Optional[str] = None
