from PIL import Image
import pytesseract

def extract_text_from_image(image_path: str, lang: str) -> str:
    image = Image.open(image_path)
    text = pytesseract.image_to_string(
        image,
        lang=lang,
        config='--tessdata-dir ~/.local/share/tessdata'
    )
    return text
