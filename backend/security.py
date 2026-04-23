from passlib.context import CryptContext

# Configuração do Argon2 (O algoritmo mais seguro atualmente)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str)-> str:
    """Transforma a senha pura em um hash seguro."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha digitada bata com o hash salvo no banco."""
    return pwd_context.verify(plain_password, hashed_password)