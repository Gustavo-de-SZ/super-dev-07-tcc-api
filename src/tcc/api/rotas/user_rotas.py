from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

#
from src.tcc.infraestrutura.banco_dados.modelos.modelo_user import ModeloUsuario
from src.tcc.infraestrutura.repositorios.usuario_repositorio import RepositorioUsuario
from src.tcc.infraestrutura.banco_dados.conexao import obter_sessao


from src.tcc.api.schemas.usuario_schema import UsuarioCriarRequest, UsuarioAlterarRequest, UsuarioResponse

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"] 
)

@router.post(
    "", 
    response_model=UsuarioResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo usuario"
)
def criar_usuario(
    dados: UsuarioCriarRequest,
    session: Session = Depends(obter_sessao)
):
   
    usuario = ModeloUsuario(
        email=dados.email,
        senha_hash=dados.senha, 
        tipo_perfil=dados.tipo_perfil.value,
        ativo=True
    )
    repositorio = RepositorioUsuario(session) 
    usuario_criado = repositorio.criar(usuario)
    return usuario_criado

@router.get(
    "",
    response_model=list[UsuarioResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios"
)
def listar_usuarios(session: Session = Depends(obter_sessao)):
    repositorio = RepositorioUsuario(session)
    usuarios = repositorio.listar()
    return usuarios

@router.get(
    "/{id}",
    response_model=UsuarioResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar usuario filtrando pelo ID"
)
def buscar_usuario(id: int, session: Session = Depends(obter_sessao)):
    repositorio = RepositorioUsuario(session)
    usuario = repositorio.buscar_por_id(id)
    if not usuario:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuario não encontrado")
    return usuario

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Inativar usuario"
)
def inativar_usuario(id: int, session: Session = Depends(obter_sessao)): 
    repositorio = RepositorioUsuario(session)
    inativou = repositorio.remover(id)
    if not inativou:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuario não encontrado")

@router.put(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Alterar dados do usuario"
)
def alterar_usuario(id: int, dados: UsuarioAlterarRequest, session: Session = Depends(obter_sessao)): 
    repositorio = RepositorioUsuario(session)
    alterou = repositorio.editar(id, dados.email) 
    if not alterou:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuario não encontrado")

@router.put(
    "/{id}/ativar",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Ativar usuario"
)
def ativar_usuario(id: int, session: Session = Depends(obter_sessao)): 
    repositorio = RepositorioUsuario(session)
    ativou = repositorio.ativar(id)
    if not ativou:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuario não encontrado.")