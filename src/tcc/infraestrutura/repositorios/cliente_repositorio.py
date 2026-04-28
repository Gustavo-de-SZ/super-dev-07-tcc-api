from sqlalchemy.orm import Session
from src.tcc.infraestrutura.banco_dados.modelos.modelo_user import ModeloUsuario, TipoPerfil
from src.tcc.infraestrutura.banco_dados.modelos.modelo_cliente import ModeloCliente

class RepositorioCliente:
    def __init__(self, sessao: Session):
        self.sessao = sessao

    def criar(self, email: str, senha_hash: str, nome_completo: str, telefone: str) -> ModeloCliente:
        usuario = ModeloUsuario(
            email=email,
            senha_hash=senha_hash,
            tipo_perfil=TipoPerfil.CLIENTE,
            ativo=True
        )
        self.sessao.add(usuario)
        self.sessao.flush()
        
        cliente = ModeloCliente(
            usuario_id=usuario.id,
            nome_completo=nome_completo,
            telefone=telefone
        )
        self.sessao.add(cliente)
        self.sessao.commit()
        self.sessao.refresh(cliente)
        return cliente

    def buscar_por_id(self, id: int) -> ModeloCliente | None:
        return self.sessao.query(ModeloCliente).filter(ModeloCliente.id == id).first()

    def buscar_por_usuario_id(self, usuario_id: int) -> ModeloCliente | None:
        return self.sessao.query(ModeloCliente).filter(ModeloCliente.usuario_id == usuario_id).first()

    def listar(self) -> list[ModeloCliente]:
        return self.sessao.query(ModeloCliente).all()

    def editar(self, id: int, nome_completo: str | None = None, telefone: str | None = None) -> bool:
        cliente = self.buscar_por_id(id)
        if not cliente:
            return False
        
        if nome_completo:
            cliente.nome_completo = nome_completo
        if telefone:
            cliente.telefone = telefone
        
        self.sessao.commit()
        return True

    def deletar(self, id: int) -> bool:
        cliente = self.buscar_por_id(id)
        if not cliente:
            return False
        
        self.sessao.delete(cliente)
        self.sessao.commit()
        return True
