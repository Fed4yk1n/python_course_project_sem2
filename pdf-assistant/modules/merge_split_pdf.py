"""
PDF Merge and Split
Author: Person 3
"""

from PyPDF2 import PdfMerger, PdfReader, PdfWriter

def merge_pdfs(pdf_paths, output_pdf_path):
    merger = PdfMerger()
    for pdf in pdf_paths:
        merger.append(pdf)
    merger.write(output_pdf_path)
    merger.close()

def split_pdf(pdf_path, output_pdf_path, start_page, end_page):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    for i in range(start_page - 1, end_page):
        writer.add_page(reader.pages[i])
    with open(output_pdf_path, 'wb') as f:
        writer.write(f)