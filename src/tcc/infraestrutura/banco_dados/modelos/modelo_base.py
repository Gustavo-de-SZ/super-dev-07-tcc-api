from sqlalchemy import Column, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    """Classe base para todos os modelos ORM."""
    pass

class ModeloBase(Base):
    """Classe abstrata com campos de auditoria (criado_em, alterado_em)"""
    __abstract__ = True

    criado_em = Column(DateTime, nullable=False, default=datetime.now)
  