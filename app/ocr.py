import httpx
from typing import Dict, Any
import base64
import io
from PIL import Image, UnidentifiedImageError
from .config import GEMINI_API_KEY

async def extract_text_from_image(image_bytes: bytes, mime_type: str) -> Dict[str, Any]:
    """
    Extrai texto de uma imagem usando a API Gemini 2.0 Flash.
    """
    if not GEMINI_API_KEY:
        return {"error": "Fora de acesso (aguarde...)"}

    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    headers = {
        "Content-Type": "application/json",
    }
    json_data = {
        "contents": [
            {
                "parts": [
                    {"text": "Extraia todo o texto desta imagem, independentemente do idioma."},
                    {"inline_data": {"mime_type": mime_type, "data": base64_image}}
                ]
            }
        ]
    }

    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(gemini_url, headers=headers, json=json_data, timeout=60.0)
            response.raise_for_status()
            response_data = response.json()

            text_parts = []
            for candidate in response_data.get("candidates", []):
                for part in candidate.get("content", {}).get("parts", []):
                    if "text" in part:
                        text_parts.append(part["text"])

            if text_parts:
                return {"extracted_text": "\n".join(text_parts)}
            else:
                return {"error": "Nenhum texto detectado na imagem ou a MorseOCR não retornou texto."}

        except httpx.RequestError as exc:
            return {"error": f"Erro de rede ou conexão ao chamar a MorseOCR: {exc}"}
        except httpx.HTTPStatusError as exc:
            return {"error": f"Erro na MorseOCR - Status: {exc.response.status_code}, Resposta: {exc.response.text}"}
        except Exception as e:
            return {"error": f"Erro inesperado ao processar a requisição com a MorseOCR: {e}"}
