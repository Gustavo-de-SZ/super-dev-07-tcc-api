from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
import enum

from .modelo_base import ModeloBase 

class TipoPerfil(enum.Enum):
    CLIENTE = "CLIENTE"
    PROFISSIONAL = "PROFISSIONAL"
    ADMIN = "ADMIN"

class ModeloUsuario(ModeloBase):
   
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable=False)
    tipo_perfil = Column(Enum(TipoPerfil), nullable=False)
    
    # Relacionamentos
    cliente = relationship("ModeloCliente", back_populates="usuario", uselist=False)
    profissional = relationship("ModeloProfissional", back_populates="usuario", uselist=False)