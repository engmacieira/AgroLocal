from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
import logging

logging.getLogger("passlib").setLevel(logging.ERROR)

# Configuração do Hashing de Senha
# O Bcrypt é muito mais seguro que o SHA256 puro porque é lento (resiste a brute force)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configurações do JWT (Em produção, viriam do .env)
SECRET_KEY = "sua_chave_secreta_super_protegida_agrolocal" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 1 dia

def create_access_token(subject: Union[str, Any]) -> str:
    """Gera um Token JWT real com tempo de expiração."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara uma senha em texto plano com o hash do banco."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera um hash seguro a partir de uma senha comum."""
    return pwd_context.hash(password)