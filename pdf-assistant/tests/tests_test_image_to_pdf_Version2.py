import unittest
import os
from modules import image_to_pdf

class TestImageToPDF(unittest.TestCase):
    def test_images_to_pdf(self):
        test_images = ["test1.jpg", "test2.png"]
        output_pdf = "test_output.pdf"
        # You need actual test images for a real test
        with self.assertRaises(Exception):
            image_to_pdf.images_to_pdf([], output_pdf)
        # Clean up if needed
        if os.path.exists(output_pdf):
            os.remove(output_pdf)

if __name__ == '__main__':
    unittest.main()