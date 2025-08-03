from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import MORSE_API_KEY

security = HTTPBearer()

async def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Função de dependência para verificar a chave de API fornecida no cabeçalho Authorization.
    Espera o formato "Bearer SUA_CHAVE".
    """
    if MORSE_API_KEY is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Chave MORSE_API_KEY não configurada no servidor."
        )

    if credentials.scheme != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Esquema de autenticação inválido. Use 'Bearer'."
        )
    if credentials.credentials != MORSE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chave de API inválida ou ausente."
        )
    return True
