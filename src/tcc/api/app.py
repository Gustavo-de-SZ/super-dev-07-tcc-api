import logging
from fastapi import FastAPI
from src.tcc.api.configuracoes import configuracoes
from src.tcc.api.rotas import user_rotas
from src.tcc.infraestrutura.banco_dados.conexao import engine
from src.tcc.infraestrutura.banco_dados.modelos.modelo_base import Base




logging.basicConfig(
    level=configuracoes.LOG_LEVEL,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H-%M-%S"
)


logger = logging.getLogger(__name__)


def criar_aplicacao() -> FastAPI:
    if configuracoes.eh_producao:
        logger.info("Iniciando aplicação em modo PRODUÇÂO (Swagger desabilitado)")
        app = FastAPI(
            docs_url=True,      # Desabilita /docs
            redoc_url=True,     # Desabilita /redoc
            openapi_url=True    # Desabilita /openapi.json
        )
    else:
        logger.info("Iniciando aplicação em modo DESENVOLVIMENTO (Swagger habilitado)")
        app = FastAPI(
            title="tcc api",
            version="1.0.0",
            docs_url="/docs",
            redoc_url="/redoc",
            openapi_url="/openapi.json",
        )




    logger.info("Registrando rotas")
    
    app.include_router(user_rotas.router, prefix="/users", tags=["Usuários"])


    @app.get("/health", tags=["Sistema"], summary="Health check", description="Verificando se a API está respondendo")
    def health_check():
        return {
            "status": "ok",
            "ambiente": configuracoes.AMBIENTE,
            "swagger_habilitado": configuracoes.swagger_habilitado
        }
    logger.info("Aplicação configurada com sucesso")
    # Base.metadata.create_all(engine)
    return app


app = criar_aplicacao()