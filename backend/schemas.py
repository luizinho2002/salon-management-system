from pydantic import BaseModel, EmailStr
from typing import Optional

# --- SCHEMAS DE USUÁRIO ---
class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: bool = False

class UserResponse(BaseModel):
    id: int
    username: str
    is_admin: bool
    is_active: bool

    class Config:
        from_attributes = True
        
# --- SCHEMAS DE CLIENTE (Novo Funcionalidade) ---
class ClientCreate(BaseModel):
    nome: str
    telefone: str
    email: Optional[EmailStr] = None
    observacoes: Optional[str] = None

class ClientResponse(ClientCreate):
    id: int

    class Config:
        from_attributes = True