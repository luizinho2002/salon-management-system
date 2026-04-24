from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional

# AVISO DE SEGURANÇA: Mantenha sua chave secreta em segredo!
# Em um ambiente de produção real, utilize variáveis de ambiente (.env)
SECRET_KEY = "sua_chave_super_segura_aqui"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_acess_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Gera um token de acesso JWT (JSON Web Token).
    """
    to_encode = data.copy()

    # Obtém o tempo atual já com o fuso horário UTC (forma moderna)
    now = datetime.now(timezone.utc)

    # Define o tempo de expiração do token
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Adiciona o campo 'exp' (expiration) aos dados do token
    to_encode.update({"exp": expire})

    # Codifica os dados e assina o token com a chave secreta
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
