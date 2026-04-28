from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .modelo_base import ModeloBase

class ModeloCliente(ModeloBase):
    
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    nome_completo = Column(String(255), nullable=False)
    telefone = Column(String(20), nullable=False)

    usuario = relationship("ModeloUsuario", back_populates="cliente")
    chamados = relationship("ModeloChamado", back_populates="cliente")