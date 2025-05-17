"""
Image to PDF Converter
Author: Person 2
"""

from PIL import Image

def images_to_pdf(image_paths, output_pdf_path):
    images = [Image.open(img).convert('RGB') for img in image_paths]
    if not images:
        raise ValueError("No images provided")
    images[0].save(output_pdf_path, save_all=True, append_images=images[1:])
    return output_pdf_path