from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

    # CORREÇÃO 1: O hash da senha é uma String longa, não um Boolean
    hashed_password = Column(String)

    # CORREÇÃO 2: Adicionar o campo is_admin que sua API vai utilizar
    is_admin = Column(Boolean, default=False)

    is_active = Column(Boolean, default=True)

# A nova tabela
class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    telefone = Column(String)
    email = Column(String, nullable=True)
    observacoes = Column(String, nullable=True)    