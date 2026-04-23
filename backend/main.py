from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, security, database

# Garante que as tabelas sejam criadas
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Salão Ivos Beauty API",
    description="Backend para gestão do salão IvosBeauty com foco em segurança",
    version="0.1.0"
)

# --- ROTAS DE USUÁRIOS ---
@app.post("/users",response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Verifica se o usuário já existe
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Este nome de usuário já está em uso.")
    
    # Gera o hash seguro da senha
    hashed_pass = security.hash_password(user.password)

    # Cria a instância do modelo
    new_user = models.User(
        username=user.username,
        hashed_password=hashed_pass,
        is_admin=user.is_admin
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Suas rotas GET antigas continuam abaixo...
@app.get("/")
async def root():
    return {"message": "API do Salão e Banco de Dados operando!"}
    
@app.get("/health")
async def health_check():
    return {"status": "healthy"}