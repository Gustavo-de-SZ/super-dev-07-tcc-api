from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.tcc.infraestrutura.banco_dados.conexao import obter_sessao
from src.tcc.infraestrutura.repositorios.cliente_repositorio import RepositorioCliente
from src.tcc.api.schemas.cliente_schema import ClienteCriarRequest, ClienteResponse

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

@router.post(
    "",
    response_model=ClienteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo cliente"
)
def criar_cliente(
    dados: ClienteCriarRequest,
    session: Session = Depends(obter_sessao)
):
    try:
        repositorio = RepositorioCliente(session)
        cliente = repositorio.criar(
            email=dados.email,
            senha_hash=dados.senha,
            nome_completo=dados.nome_completo,
            telefone=dados.telefone,
            cpf=dados.cpf
        )
        return cliente
    except IntegrityError as e:
        session.rollback()
        if "email" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email já cadastrado"
            )
        elif "cpf" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="CPF já cadastrado"
            )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Erro ao criar cliente: dados duplicados"
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar cliente: {str(e)}"
        )

@router.get(
    "",
    response_model=list[ClienteResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar clientes"
)
def listar_clientes(session: Session = Depends(obter_sessao)):
    repositorio = RepositorioCliente(session)
    clientes = repositorio.listar()
    return clientes

@router.get(
    "/{id}",
    response_model=ClienteResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar cliente por ID"
)
def buscar_cliente(id: int, session: Session = Depends(obter_sessao)):
    repositorio = RepositorioCliente(session)
    cliente = repositorio.buscar_por_id(id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    return cliente

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar cliente"
)
def deletar_cliente(id: int, session: Session = Depends(obter_sessao)):
    repositorio = RepositorioCliente(session)
    deletou = repositorio.deletar(id)
    if not deletou:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
