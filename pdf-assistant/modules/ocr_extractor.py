"""
PDF OCR Text Extraction
Author: Person 4
"""

import pytesseract
from pdfplumber import open as pdfplumber_open
from PIL import Image
import io

def ocr_pdf(pdf_path):
    text = ""
    with pdfplumber_open(pdf_path) as pdf:
        for page in pdf.pages:
            # Try OCR on the rasterized page
            img = page.to_image(resolution=300)
            img_buf = io.BytesIO()
            img.original.save(img_buf, format="PNG")
            img_buf.seek(0)
            image = Image.open(img_buf)
            text += pytesseract.image_to_string(image)
            # Optionally, also extract text via PDF if available
            extracted = page.extract_text()
            if extracted:
                text += "\n" + extracted
    return text
