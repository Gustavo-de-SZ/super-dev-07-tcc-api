from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class ClienteBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    telefone: Optional[str] = Field(None, max_length=20)
    empresa: Optional[str] = Field(None, max_length=255)
    local: str  # full address string built by the frontend
    avaliacao: Optional[int] = Field(0, ge=0, le=5)
    servicosAtivos: Optional[int] = Field(0, ge=0)
    servicosConcluidos: Optional[int] = Field(0, ge=0)

class ClienteCriarRequest(ClienteBase):
    senha: str = Field(..., min_length=6)   # required for regular users

class ClienteCreateTech(ClienteBase):
    # No senha field - technician-created client
    pass

class ClienteAuth0Request(ClienteBase):
    # No senha field - Auth0 managed
    tipoCliente: str
    status: str = 'Ativo'

    class Config:
        extra = 'allow'  # Allow extra fields from frontend

class ClienteResponse(BaseModel):
    id: int
    usuario_id: int
    nome_completo: str
    telefone: str
    criado_em: datetime
    email: str
    ativo: bool
    empresa: str | None = None
    avaliacao: int = 0
    servicos_ativos: int = 0
    servicos_concluidos: int = 0
    endereco: str | None = None

    class Config:
        from_attributes = True

class EstatisticaClienteResponse(BaseModel):
    total: int
    ativosEsteMes: int
    novosEsteMes: int

    class Config:
        from_attributes = True