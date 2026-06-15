from PIL import Image
import easyocr
import numpy as np

# Create OCR reader once when the application starts
reader = easyocr.Reader(['en'], gpu=False)


def extract_text(file_bytes):
    """
    Extract text from an uploaded image.
    """

    image = Image.open(file_bytes)

    image_np = np.array(image)

    results = reader.readtext(image_np)

    extracted_text = []

    for result in results:
        extracted_text.append(result[1])

    return extracted_text