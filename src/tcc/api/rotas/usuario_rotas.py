from http import HTTPStatus
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid6 import uuid7

from bem_saude.api.schemas.recepcionista_schemas import RecepcionistaAlterarRequest, RecepcionistaCriarRequest, RecepcionistaResponse
from bem_saude.infraestrutura.banco_dados.conexao import obter_sessao
from bem_saude.infraestrutura.banco_dados.modelos.modelo_recepcionista import ModeloRecepcionista
from bem_saude.infraestrutura.repositorios.repositorio_recepcionista import RepositorioRecepcionista

# Router para endpoints de recepcionistas
# Todas as rotas começam com /recepcionistas

router = APIRouter(
    prefix="/usuarios",
    tags=["Recepcionista"]
)
@router.post(
    "", 
    response_model=RecepcionistaResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo usuario",
    responses={
        201: {
            "description": "usuario criado com sucesso",
            "model": usuarioResponse
        }
    }
)
def criar_usuario(
    dados: usuarioCriarRequest,
    session: Session = Depends(obter_sessao)) -> usuarioResponse:
    usuario = Modelousuario(
        id=uuid7(),
        nome=dados.nome,
        status=dados.status,
    )
    repositorio = RepositorioUsuario(sessao=session)
    usuario = repositorio.criar(usuario)
    return usuario


@router.get(
    "",
    response_model=list[usuarioResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    responses={
        200: {
            "description": "Lista de usuarios",
            "model": list[usuarioResponse]
        },
    },
)
def listar_usuarios(session: Session = Depends(obter_sessao)):
    """Lista todos os usuarios"""
    repositorio = RepositorioUsuario(sessao=session)
    usuarios = repositorio.listar()
    return usuarios


@router.get(
    "/{id}",
    response_model=usuarioResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar usuario filtrando pelo ID",
    description="""
            Busca um usuario específico pelo seu ID  (UUID v7).
            
            Retorna todos os dados do usuario, incluido campos de auditoria.""",
    responses={
        200: {
            "description": "usuario encontrado",
            "model": usuarioResponse
        },
    },
)
def buscar_usuario(id: UUID, session: Session = Depends(obter_sessao)):
    """Busca um usuario por ID."""
    repositorio = RepositorioUsuario(sessao=session)
    usuario = repositorio.buscar_por_id(id)
    if not usuario:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="usuario não encontrado")
    return usuario


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Inativar usuario",
    description="Inativar o usuario quando encontrado.",
    responses={
        204: {
            "description": "usuario inativado",
        },
    },
)
def inativar_usuario(id: UUID, session: Session = Depends(obter_sessao)):
    """Inativa um usuario por ID."""
    repositorio = RepositorioUsuario(sessao=session)
    inativou = repositorio.remover(id)
    if not inativou:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="usuario não encontrado")


@router.put(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Alterar dados do usuario",
    responses={
        204: {
            "description": "usuario alterado"
        },
        404: {
            "description": "usuario não encontrado"
        }
    }
)
def alterar_usuario(id: UUID, dados: usuarioAlterarRequest, session: Session = Depends(obter_sessao)):
    repositorio = RepositorioUsuario(sessao=session)
    alterou = repositorio.editar(id, dados.nome)
    if not alterou:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="usuario não encontrado")
    

@router.put(
    "/{id}/ativar",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Ativar usuario",
    responses={
        204: {
            "description": "usuario ativado com sucesso"
        },
        404: {
            "description": "usuario não encontrado"
        },
    },
)
def ativar_usuario(
    id: UUID,
    session: Session = Depends(obter_sessao),
):
    repositorio = RepositorioUsuario(sessao=session)

    ativou = repositorio.ativar(id)
    if not ativou:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="usuario não encontrado."
        )
