"""
PDF Security: Password, Watermark, Signature
Author: Person 6
"""

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfMerger
import io

def add_password(pdf_path, output_pdf_path, password):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(password)
    with open(output_pdf_path, 'wb') as f:
        writer.write(f)

def remove_password(pdf_path, output_pdf_path, password):
    reader = PdfReader(pdf_path, password=password)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    with open(output_pdf_path, 'wb') as f:
        writer.write(f)

def add_watermark(pdf_path, watermark_pdf_path, output_pdf_path):
    reader = PdfReader(pdf_path)
    watermark = PdfReader(watermark_pdf_path).pages[0]
    writer = PdfWriter()
    for page in reader.pages:
        page.merge_page(watermark)
        writer.add_page(page)
    with open(output_pdf_path, 'wb') as f:
        writer.write(f)

def add_signature(pdf_path, signature_image_path, output_pdf_path):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    for page in reader.pages:
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.drawImage(signature_image_path, 100, 100, 150, 50, mask='auto')
        can.save()
        packet.seek(0)
        watermark = PdfReader(packet).pages[0]
        page.merge_page(watermark)
        writer.add_page(page)
    with open(output_pdf_path, 'wb') as f:
        writer.write(f)