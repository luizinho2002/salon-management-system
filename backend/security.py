
from fastapi.security import OAuth2PasswordBearer

# Este comando indica ao FastAPI que a rota para obter o token "/token"
# O Swagger utilizará isso para saber onde enviar o usuário e senha
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")