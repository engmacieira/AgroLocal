from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from uuid import UUID
from app.domain.entities.user import UserRole

class UserRegisterRequest(BaseModel):
    """Schema de Entrada: Valida os dados recebidos na requisição (JSON)."""
    email: EmailStr # O Pydantic já valida se é um e-mail válido!
    password: str = Field(..., min_length=6, description="A senha deve ter no mínimo 6 caracteres")
    full_name: str = Field(..., min_length=2)
    role: UserRole = UserRole.CLIENTE
    phone: Optional[str] = None

class UserUpdateRequest(BaseModel):
    """Schema de Entrada: Dados permitidos para atualização de perfil."""
    full_name: Optional[str] = Field(None, min_length=2)
    phone: Optional[str] = None

class UserLoginRequest(BaseModel):
    """Schema para receber as credenciais de login."""
    email: EmailStr
    password: str = Field(..., min_length=6)

class TokenResponse(BaseModel):
    """Schema para devolver o Token de Acesso."""
    access_token: str
    token_type: str
    
class UserResponse(BaseModel):
    """Schema de Saída: Filtra o que será devolvido na resposta (JSON). NUNCA devolva a senha!"""
    id: UUID
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    is_verified: bool
    
    model_config = ConfigDict(from_attributes=True)

