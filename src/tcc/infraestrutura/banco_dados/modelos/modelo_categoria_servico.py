from sqlalchemy import Column, String, Integer, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
import enum
from .modelo_base import ModeloBase

class StatusChamado(enum.Enum):
    ABERTO = "ABERTO"             
    EM_ANDAMENTO = "EM_ANDAMENTO" 
    CONCLUIDO = "CONCLUIDO"       
    CANCELADO = "CANCELADO"       

class ModeloChamado(ModeloBase):
    """Mapeia os tickets de suporte e solicitações de serviço"""
    __tablename__ = "chamados"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Chaves Estrangeiras
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    profissional_id = Column(Integer, ForeignKey("profissionais.id"), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias_servico.id"), nullable=False)
    
    titulo = Column(String(255), nullable=False)
    descricao_problema = Column(Text, nullable=False)
    status = Column(Enum(StatusChamado), default=StatusChamado.ABERTO)
    
    # Relacionamentos
    cliente = relationship("ModeloCliente", back_populates="chamados")
    profissional = relationship("ModeloProfissional", back_populates="chamados")
    categoria = relationship("ModeloCategoriaServico", back_populates="chamados")