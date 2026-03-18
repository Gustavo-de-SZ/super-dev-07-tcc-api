from uuid import UUID
from sqlalchemy.orm import Session
from src.tcc.infraestrutura.banco_dados.modelos.modelo_user import ModeloUsuario

class RepositorioUsuario:
    def __init__(self, sessao: Session):
        self.sessao = sessao


    def criar(self, usuario: ModeloUsuario) -> ModeloUsuario:
        self.sessao.add(usuario)
        self.sessao.commit()
        self.sessao.flush(usuario)

        return usuario
    

    def editar(
            self,
            id: UUID,
            nome: str,
            telefone: str,
            endereco: str,
            observacoes: str,
            email: str):
        modelo = self.sessao.query(ModeloUsuario).filter(ModeloUsuario.id == id).first()
        if not modelo:
            return False
        
        modelo.nome = nome
        modelo.telefone = telefone
        modelo.endereco = endereco
        modelo.observacoes = observacoes
        modelo.email = email

        self.sessao.commit()
        return True
    

    def inativar(self, id: UUID):
        usuario = self.sessao.query(ModeloUsuario).filter(ModeloUsuario.id == id).first()
        if not usuario:
            return False
        
        usuario.status = "INATIVO"
        self.sessao.commit()
        return True
    

    def ativar(self, id: UUID):
        usuario = self.sessao.query(ModeloUsuario).filter(ModeloUsuario.id == id).first()
        if not usuario:
            return False
        
        usuario.status = "ATIVO"
        self.sessao.commit()
        return True
    

    def listar(self) -> list[ModeloUsuario]:
        usuarios = self.sessao.query(ModeloUsuario).order_by(ModeloUsuario.status, ModeloUsuario.nome).all()

        return usuarios

    
    def buscar_por_id(self, id: UUID) -> ModeloUsuario | None:
        usuario = self.sessao.query(ModeloUsuario).filter(ModeloUsuario.id == id).first()
        if not usuario:
            return False
        
        return usuario