from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.tcc.infraestrutura.banco_dados.conexao import obter_sessao
from src.tcc.infraestrutura.repositorios.profissional_repositorio import RepositorioProfissional
from src.tcc.api.schemas.profissional_schema import ProfissionalCriarRequest, ProfissionalResponse

router = APIRouter(
    prefix="/profissionais",
    tags=["Profissionais"]
)

@router.post(
    "",
    response_model=ProfissionalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo profissional"
)
def criar_profissional(
    dados: ProfissionalCriarRequest,
    session: Session = Depends(obter_sessao)
):
    try:
        repositorio = RepositorioProfissional(session)
        profissional = repositorio.criar(
            email=dados.email,
            senha_hash=dados.senha,
            nome_fantasia=dados.nome_fantasia,
            cpf=dados.cpf,
            telefone=dados.telefone,
            descricao_servicos=dados.descricao_servicos
        )
        return profissional
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
            detail="Erro ao criar profissional: dados duplicados"
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar profissional: {str(e)}"
        )

@router.get(
    "",
    response_model=list[ProfissionalResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar profissionais"
)
def listar_profissionais(session: Session = Depends(obter_sessao)):
    repositorio = RepositorioProfissional(session)
    profissionais = repositorio.listar()
    return profissionais

@router.get(
    "/aprovados",
    response_model=list[ProfissionalResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar profissionais aprovados"
)
def listar_profissionais_aprovados(session: Session = Depends(obter_sessao)):
    repositorio = RepositorioProfissional(session)
    profissionais = repositorio.listar_aprovados()
    return profissionais

@router.get(
    "/{id}",
    response_model=ProfissionalResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar profissional por ID"
)
def buscar_profissional(id: int, session: Session = Depends(obter_sessao)):
    repositorio = RepositorioProfissional(session)
    profissional = repositorio.buscar_por_id(id)
    if not profissional:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profissional não encontrado"
        )
    return profissional

@router.patch(
    "/{id}/aprovar",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Aprovar profissional pelo admin"
)
def aprovar_profissional(id: int, session: Session = Depends(obter_sessao)):
    repositorio = RepositorioProfissional(session)
    aprovou = repositorio.aprovar(id)
    if not aprovou:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profissional não encontrado"
        )

@router.patch(
    "/{id}/rejeitar",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Rejeitar profissional"
)
def rejeitar_profissional(id: int, session: Session = Depends(obter_sessao)):
    repositorio = RepositorioProfissional(session)
    rejeitou = repositorio.rejeitar(id)
    if not rejeitou:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profissional não encontrado"
        )

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar profissional"
)
def deletar_profissional(id: int, session: Session = Depends(obter_sessao)):
    repositorio = RepositorioProfissional(session)
    deletou = repositorio.deletar(id)
    if not deletou:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profissional não encontrado"
        )
