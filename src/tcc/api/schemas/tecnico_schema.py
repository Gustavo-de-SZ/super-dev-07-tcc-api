from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class TecnicCreateRequest(BaseModel):
    email: EmailStr
    nome: str  # will be used as nome_fantasia
    # optional fields that may be provided later
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    descricao_servicos: Optional[str] = None

    class Config:
        # Allow extra fields to be ignored (not cause validation error)
        extra = 'ignore'

class TecnicResponse(BaseModel):
    id: int
    usuario_id: int
    nome_fantasia: str
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    descricao_servicos: Optional[str] = None
    aprovado_pelo_admin: bool
    criado_em: datetime
    email: str

    class Config:
        from_attributes = True