from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


URL_CONEXAO = "mysql+mysqlconnector://root:I1e1l2@localhost/tcc"

engine = create_engine(URL_CONEXAO)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def obter_sessao():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
# uvicorn src.tcc.principal:app --reload