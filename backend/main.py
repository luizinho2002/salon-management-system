from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, security, database
# Importando as funções do seu auth.py
from auth import authenticate_user, create_access_token

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

# --- ROTAS DE CLIENTES ---
@app.post("/clients", response_model=schemas.ClientResponse)
def create_client(client: schemas.ClientCreate, db: Session = Depends(database.get_db)):
    # Cria a instância do modelo Client com os dados recebidos
    new_client = models.Client(
        nome=client.nome,
        telefone=client.telefone,
        email=client.email,
        observacoes=client.observacoes
    )

    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

@app.get("/clients", response_model=list[schemas.ClientResponse])
def get_clients(db: Session = Depends(database.get_db)):
    # Retorna todas as clientes cadastradas
    return db.query(models.Client).all()


# --- ATUALIZAR CLIENTE (UPDATE) ---
@app.put("/clients/{clients_id}", response_model=schemas.ClientResponse)
def update_client(client_id: int, updated_data: schemas.ClientCreate, db: Session = Depends(database.get_db)):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()

    if not db_client:
        raise HTTPException(status_code=404, detail="Cliente não encontrada.")
    
    # Atualiza os campos
    db_client.nome = updated_data.nome
    db_client.telefone = updated_data.telefone
    db_client.email = updated_data.email
    db_client.observacoes = updated_data.observacoes

    db.commit()
    db.refresh(db_client)
    return db_client

# --- DELETAR CLIENTE (DELETE) ---
@app.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(database.get_db)):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first() 

    if not db_client:
        raise HTTPException(status_code=404, detail="Cliente não encontrada.")
    
    db.delete(db_client)
    db.commit()
    return {"message": f"Cliente {client_id} removida com sucesso!"}

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Tenta autenticar o usuário com a lógica do auth.py
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"www-Authenticate": "Bearer"},
        )

    # Se passar, gera o Token JWT
    access_token = create_access_token(data={"sub": user["username"]})

    return {"acess_token": access_token, "token_type": "bearer"} 

# Suas rotas GET antigas continuam abaixo...
@app.get("/")
async def root():
    return {"message": "API do Salão e Banco de Dados operando!"}
    
@app.get("/health")
async def health_check():
    return {"status": "healthy"}