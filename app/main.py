from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp
import io
from PIL import Image, UnidentifiedImageError

from .auth import verify_api_key
from .ocr import extract_text_from_image
from .config import ALLOWED_ORIGINS, SECURITY_HEADERS

app = FastAPI(
    title="MorseOCR API",
    description="API para extrair texto de imagens usando Google Gemini 2.0 Flash.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        for header, value in SECURITY_HEADERS.items():
            response.headers[header] = value
        return response

app.add_middleware(SecurityHeadersMiddleware)

@app.get("/", include_in_schema=False)
async def read_root():
    return {"message": "Bem-vindo a  MorseOCR. Acesse /docs para a documentação interativa."}

@app.post(
    "/ocr/image",
    summary="Extrair texto de uma imagem",
    response_description="Texto extraído da imagem em formato JSON",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_api_key)]
)
async def process_image_for_ocr(
    file: UploadFile = File(..., description="Imagem para processar (JPG ou PNG).")
):
    allowed_content_types = ["image/jpeg", "image/png, "]
    if file.content_type not in allowed_content_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato de arquivo não suportado. Apenas imagens JPG ({allowed_content_types[0]}) e PNG ({allowed_content_types[1]}) são aceitas. Tipo recebido: {file.content_type}"
        )

    try:
        image_bytes = await file.read()
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img.verify()
            img = Image.open(io.BytesIO(image_bytes))
            img.close()
        except UnidentifiedImageError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O arquivo fornecido não é uma imagem válida ou está corrompido."
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao validar a imagem: {e}"
            )

        ocr_result = await extract_text_from_image(image_bytes, file.content_type)

        if "error" in ocr_result:
            if "Fora de acesso, (volte mais tarde...)" in ocr_result["error"]:
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            elif "Nenhum texto detectado" in ocr_result["error"]:
                status_code = status.HTTP_204_NO_CONTENT
            elif "Erro de rede" in ocr_result["error"] or "Erro na API Gemini" in ocr_result["error"]:
                status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            else:
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            return JSONResponse(status_code=status_code, content=ocr_result)
        else:
            return JSONResponse(status_code=status.HTTP_200_OK, content=ocr_result)

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Erro inesperado no endpoint /ocr/image: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro interno inesperado ao processar a imagem: {str(e)}"
        )


"""
MorceOCR - Plataforma de OCR inteligente e rápida para imagens

Desenvolvido por:
- Morse

Data de criação: Agosto de 2025

Descrição:
Este sistema realiza reconhecimento de texto (OCR) diretamente a partir de imagens, 
com foco em velocidade, simplicidade e acessibilidade via navegador. 
A ferramenta é ideal para uso educacional, profissional e cotidiano, sem necessidade de cadastro.

Contato oficial:
- Email: morse.official.mail@gmail.com
- País: Moçambique

Observações:
Este projeto é experimental e ainda está em desenvolvimento. O uso deve respeitar as 
leis locais e internacionais aplicáveis. A versão atual não utiliza nenhuma licença formal.
"""
