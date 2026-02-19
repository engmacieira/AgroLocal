from pydantic import EmailStr, Field, ConfigDict
from typing import Optional
from uuid import UUID
from app.models.user_model import UserRole
from app.schemas.base_schema import BaseSchema, TimestampSchema

# --- Schemas de Perfil (Producer) ---

class ProducerProfileBase(BaseSchema):
    """
    Dados específicos para parceiros que vendem na plataforma (Agricultores).
    """
    cpf_cnpj: str = Field(
        ..., 
        min_length=11, 
        max_length=14,
        pattern=r"^\d+$", # Apenas números
        description="CPF (11 dígitos) ou CNPJ (14 dígitos) sem pontuação",
        examples=["12345678901"]
    )
    
    pix_key: str = Field(
        ..., 
        max_length=100,
        description="Chave PIX para recebimento dos repasses (E-mail, CPF, Aleatória)",
        examples=["joao@fazenda.com"]
    )
    
    store_name: str = Field(
        ..., 
        min_length=3, 
        max_length=100,
        description="Nome fantasia da loja/sítio visível no App",
        examples=["Sítio Recanto Verde"]
    )
    
    bio: Optional[str] = Field(
        default=None, 
        max_length=500,
        description="Breve história do produtor ou do sítio (Marketing)",
        examples=["Produzimos hortaliças orgânicas desde 1990."]
    )

class ProducerProfileCreate(ProducerProfileBase):
    """Payload para criar o perfil de produtor (geralmente aninhado no UserCreate)."""
    pass

class ProducerProfileRead(ProducerProfileBase):
    """Visualização pública do perfil do produtor."""
    id: UUID = Field(description="ID único do perfil")
    rating: float = Field(description="Média de avaliações (0.0 a 5.0)")
    review_count: int = Field(description="Total de avaliações recebidas")

# --- Schemas de Usuário (Conta de Acesso) ---

class UserBase(BaseSchema):
    """
    Dados base do utilizador (Comuns a Clientes e Produtores).
    """
    email: EmailStr = Field(
        ..., 
        description="E-mail válido para login e notificações"
    )
    
    full_name: str = Field(
        ..., 
        min_length=3, 
        max_length=100,
        description="Nome completo do utilizador",
        examples=["João da Silva"]
    )
    
    phone: Optional[str] = Field(
        default=None, 
        max_length=20,
        description="Telefone para contacto (Preferencialmente WhatsApp)",
        examples=["(11) 99999-9999"]
    )
    
    role: UserRole = Field(
        default=UserRole.CLIENTE,
        description="Tipo de conta: CLIENTE (Comprador), PRODUTOR (Vendedor) ou ADMIN"
    )

class UserCreate(UserBase):
    """
    Payload para registo de novos utilizadores (Sign Up).
    Suporta a criação simultânea do perfil de produtor.
    """
    password: str = Field(
        ..., 
        min_length=8,
        description="Senha forte (Mínimo 8 caracteres)",
        examples=["SenhaForte@123"]
    )
    
    # Campo opcional: Só envia se for registar um PRODUTOR
    producer_profile: Optional[ProducerProfileCreate] = Field(
        default=None,
        description="Dados extras obrigatórios APENAS se role='PRODUTOR'"
    )

    # Exemplo Rico: Cadastro de um Produtor Completo
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "email": "joao@fazenda.com",
                    "full_name": "João Agricultor",
                    "phone": "(12) 99999-1234",
                    "role": "PRODUTOR",
                    "password": "senha_segura_123",
                    "producer_profile": {
                        "cpf_cnpj": "12345678901",
                        "pix_key": "joao@pix.com",
                        "store_name": "Sítio do João",
                        "bio": "Produtos frescos colhidos na hora."
                    }
                }
            ]
        }
    )

class UserRead(UserBase, TimestampSchema):
    """
    Retorno seguro dos dados do utilizador (Nunca devolve a senha).
    """
    id: UUID = Field(description="ID único do utilizador")
    
    is_active: bool = Field(description="A conta está ativa?")
    is_verified: bool = Field(description="O e-mail foi confirmado?")
    
    avatar_url: Optional[str] = Field(
        default=None,
        description="URL da foto de perfil"
    )
    
    # Retorna o perfil aninhado se existir
    producer_profile: Optional[ProducerProfileRead] = Field(
        default=None,
        description="Perfil de vendedor (presente apenas se role='PRODUTOR')"
    )

class UserUpdate(BaseSchema):
    """
    Campos permitidos para atualização de perfil pelo próprio utilizador.
    """
    full_name: Optional[str] = Field(None, min_length=3, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = None
    
    # Nota: A troca de senha geralmente é feita em rota específica, 
    # mas mantemos aqui para flexibilidade se necessário.
    password: Optional[str] = Field(None, min_length=8, description="Nova senha (opcional)")