from PIL import Image
import pytesseract


def extract_text(file_bytes):
    image = Image.open(file_bytes)
    text = pytesseract.image_to_string(image)

    return [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]