from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Nome do arquivo do banco que será criado automaticamente
SQLALCHEMY_DATABASE_URL = "sqlite:///./salao.db"

# Engine: O motor que conversa com o arquivo .db
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal: Cada requisição ao app terá sua própria sessão de banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: Classa que nossas tabelas vão herdar
Base = declarative_base()

# Dependência para obter o banco nas rotas da API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()