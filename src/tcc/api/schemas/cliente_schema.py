from pydantic import BaseModel, EmailStr
from datetime import datetime

class ClienteCriarRequest(BaseModel):
    email: EmailStr
    senha: str
    nome_completo: str
    telefone: str

class ClienteResponse(BaseModel):
    id: int
    usuario_id: int
    nome_completo: str
    telefone: str
    criado_em: datetime
    email: str
    ativo: bool

    class Config:
        from_attributes = True
