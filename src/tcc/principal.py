from fastapi import FastAPI
from src.tcc.api.rotas import user_rotas
from src.tcc.infraestrutura.banco_dados.conexao import engine
from src.tcc.infraestrutura.banco_dados.modelos.modelo_base import Base




app = FastAPI(
    title="API ",
    description="Backend TCC",
)


app.include_router(user_rotas.router)

@app.get("/")
def root():
    return {"api": "Online"}