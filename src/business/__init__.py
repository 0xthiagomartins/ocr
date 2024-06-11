import pytesseract
from PIL import Image
import io


def perform_ocr(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image)
    return text
