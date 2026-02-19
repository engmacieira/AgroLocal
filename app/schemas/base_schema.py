from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class BaseSchema(BaseModel):
    """
    Classe base para todos os Schemas Pydantic do AgroLocal.
    
    Configurações Globais:
    - from_attributes=True: Permite converter objetos ORM (SQLAlchemy) diretamente para Schemas.
      Isso habilita o uso de métodos como `UserRead.model_validate(user_db_obj)`.
    """
    model_config = ConfigDict(from_attributes=True)

class TimestampSchema(BaseSchema):
    """
    Mixin para adicionar campos de auditoria temporal (created_at, updated_at).
    Deve ser herdado por Schemas de Leitura (Read) que precisam expor quando o registro foi criado.
    """
    created_at: Optional[datetime] = Field(
        default=None,
        description="Data e hora exata da criação do registro",
        examples=["2026-02-18T14:00:00Z"]
    )
    
    updated_at: Optional[datetime] = Field(
        default=None,
        description="Data e hora da última alteração no registro",
        examples=["2026-02-19T10:30:00Z"]
    )