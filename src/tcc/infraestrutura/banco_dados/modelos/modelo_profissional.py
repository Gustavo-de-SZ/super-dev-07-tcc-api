from sqlalchemy import Column, String, Integer, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from .modelo_base import ModeloBase

class ModeloProfissional(ModeloBase):
    __tablename__ = "profissionais"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    nome_fantasia = Column(String(255), nullable=False)
    documento = Column(String(20), unique=True, nullable=False)
    telefone = Column(String(20), nullable=False)
    descricao_servicos = Column(Text, nullable=True)
    aprovado_pelo_admin = Column(Boolean, default=False)

    usuario = relationship("ModeloUsuario", back_populates="profissional")
    itens_inventario = relationship("ModeloInventario", back_populates="profissional")