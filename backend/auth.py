from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional
import bcrypt # Mudança aqui: utilizando bcrypt puro para evitar erros no Python 3.13

# --- CONFIGURAÇÕES DE SEGURANÇA ---
SECRET_KEY = "sua_chave_super_secreta_aqui"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- FUNÇÕES DE SENHA (BCRYPT PURO) ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha concide com o hash utilizando bytes (padrão 3.13)"""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def get_password_hash(password: str) -> str:
    """Gera um hash seguro convertendo a string para bytes antes de processar."""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')

# --- FUNÇÕES DE JWT (TOKEN) ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Gera um token JWT corrigindo o erro de comparação de datetime."""
    to_encode = data.copy()

    # Utilizando timezone.utc para evitar conflitos de fuso horário
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # O segredo: converter o datetime em timestamp (número) para o JWT
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- LÓGICA DE AUTENTICAÇÃO ---
def authenticate_user(username, password):
    # Dicionário de teste - Garanta que as chaves estão escritas corretamente
    user_db = {
        "admin": {
            "username": "admin",
            "hashed_password": get_password_hash("123456")
        }
    }

    # Busca o usuário pelo nome (chave do dicionário)
    user = user_db.get(username)

    # Se não encontrar o usuário, retorna False
    if not user:
        return False
    
    # Agora buscamos a senha dentro do dicionário do usuário encontrado
    # O erro 'KeyError' acontecia aqui se o nome da chave estivesse diferente
    hashed_pwd = user.get("hashed_password")

    if not hashed_pwd or not verify_password(password, hashed_pwd):
        return False
    
    return user