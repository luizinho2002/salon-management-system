from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from typing import Optional
from passlib.context import CryptContext

# --- CONFIGURAÇÕES DE SEGURANÇA ---
# Futuramente, utilize: os.getenv("SECRET_KEY")
SECRET_KEY = "sua_chave_super_segura_aqui"
ALGORITHM  = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuração do Hash de Senha (Bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- FUNÇÕES DE SENHA ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto puro coincide com o hash do banco."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera um hash seguro da senha para ser salvo no banco de dados.""" 
    return pwd_context.hash(password)

# --- FUNÇÕES DE JWT (TOKEN) ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Gera um token de acesso JWT com tempo de expiração."""
    to_encode = data.copy()
    now = datetime.now(timezone.utc)

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- LÓGICA DE AUTENTICAÇÃO ---
def authenticate_user(username, password):
    # Dicionário de teste
    user_db = {
        "admin": {
            "username": "admin",
            "hashed_password": get_password_hash("123456")
        }
    }

    user = user_db.get(username)
    if not user:
        return False
    
    # IMPORTANTE: Verifique se os nomes das funções batem
    if not verify_password(password, user["hashed_password"]):
        return False
    
    return user