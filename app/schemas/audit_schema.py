from typing import Optional, Any, Dict
from uuid import UUID
from datetime import datetime
from pydantic import Field, ConfigDict

from app.models.audit_model import AuditAction
from app.schemas.base_schema import BaseSchema

class AuditLogRead(BaseSchema):
    """
    Schema de Leitura para Logs de Auditoria.
    Representa um registro imutável de uma ação ocorrida no sistema.
    """
    id: UUID = Field(
        description="Identificador único do log"
    )
    
    table_name: str = Field(
        ..., 
        description="Nome da tabela onde ocorreu a alteração",
        examples=["products", "orders", "users"]
    )
    
    # Nota: No model original estava Integer, mas aqui estamos usando UUID 
    # para suportar o padrão do projeto. Certifique-se que o banco suporta.
    record_id: UUID = Field(
        ..., 
        description="ID do registro que foi alterado (Foreign Key lógica)"
    )
    
    action: AuditAction = Field(
        ..., 
        description="Tipo de ação executada (CREATE, UPDATE, DELETE, etc.)"
    )
    
    actor_id: Optional[UUID] = Field(
        default=None, 
        description="ID do usuário responsável pela ação (Null se for ação do sistema)"
    )
    
    ip_address: Optional[str] = Field(
        default=None, 
        description="Endereço IP de origem da requisição",
        examples=["192.168.1.50", "2001:0db8:85a3:0000:0000:8a2e:0370:7334"]
    )
    
    user_agent: Optional[str] = Field(
        default=None, 
        description="Assinatura do navegador/dispositivo do usuário",
        examples=["Mozilla/5.0 (iPhone; CPU iPhone OS 14_0...)"]
    )
    
    # Delta de mudanças
    old_values: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Estado dos dados ANTES da alteração (Apenas para UPDATE/DELETE)"
    )
    
    new_values: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Estado dos dados DEPOIS da alteração (Para CREATE/UPDATE)"
    )
    
    created_at: datetime = Field(
        description="Data e hora exata do evento"
    )

    # Configuração para Documentação Automática (Swagger UI)
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                    "table_name": "producer_products",
                    "record_id": "b2f4c810-1d2a-4f5b-9c8e-2a3b4c5d6e7f",
                    "action": "UPDATE",
                    "actor_id": "c3d5e712-3a4b-5c6d-7e8f-9a0b1c2d3e4f",
                    "ip_address": "203.0.113.42",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
                    "old_values": {
                        "price": 10.00,
                        "stock_quantity": 50
                    },
                    "new_values": {
                        "price": 12.50,
                        "stock_quantity": 45
                    },
                    "created_at": "2026-02-18T15:30:00Z"
                }
            ]
        }
    )