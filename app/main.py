from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from app.ocr import extract_text_from_image
import os, uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trocar para o domínio do front-end em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE_MB = 2
ALLOWED_EXTENSIONS = {
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/webp"
}
ALLOWED_LANGUAGES = {"por", "eng", "fra", "spa"}


@app.get("/")
def root():
    return {"status": "online", "message": "MorseOCR API funcionando!"}

@app.post("/ocr/image")
async def ocr_image(
    file: UploadFile = File(...),
    lang: str = Query("por", description="Idioma do texto na imagem (por, eng, spa, fra)")
):
    if file.content_type not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Formato de imagem não suportado. Use PNG, JPG ou JPEG.")

    if lang not in ALLOWED_LANGUAGES:
        raise HTTPException(status_code=400, detail="Idioma não suportado. Use por, eng, spa ou fra.")

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Imagem muito grande. Máximo permitido: 2MB.")

    temp_filename = f"static/{uuid.uuid4().hex}.jpg"
    with open(temp_filename, "wb") as f:
        f.write(contents)

    text = extract_text_from_image(temp_filename, lang)
    os.remove(temp_filename)

    return {"text": text.strip()}
