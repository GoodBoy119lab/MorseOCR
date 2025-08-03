import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configurações da API ---
# Chave de autenticação para a API MorseOCR
MORSE_API_KEY = os.getenv("MORSE_API_KEY")

# Chave da API Google Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Domínios permitidos para CORS (Cross-Origin Resource Sharing)
# Em um ambiente de produção, substituiremos  por nossos domínios reais.
ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Headers de segurança para proteção contra ataques comuns
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Content-Security-Policy": "default-src 'self'",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Referrer-Policy": "no-referrer-when-downgrade",
}

if not MORSE_API_KEY:
    print("AVISO: Variável de ambiente MORSE_API_KEY não configurada. A API não funcionará corretamente sem ela.")
if not GEMINI_API_KEY:
    print("AVISO: Variável de ambiente GEMINI_API_KEY não configurada. A funcionalidade OCR não funcionará.")

## Facilitar a vida de outros programadores, com a facil leitura dos codigos é uma torta bem feita, Sandino Januário!
