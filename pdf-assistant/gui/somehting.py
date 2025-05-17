import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from modules import image_to_pdf, merge_split_pdf, ocr_extractor, security

class PDFAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Assistant")
        self.create_widgets()

    def create_widgets(self):
        btn1 = tk.Button(self.root, text="Image(s) to PDF", width=30, command=self.image_to_pdf_ui)
        btn2 = tk.Button(self.root, text="Merge PDFs", width=30, command=self.merge_pdf_ui)
        btn3 = tk.Button(self.root, text="Split PDF", width=30, command=self.split_pdf_ui)
        btn4 = tk.Button(self.root, text="Extract Text (OCR)", width=30, command=self.ocr_ui)
        btn6 = tk.Button(self.root, text="PDF Security", width=30, command=self.security_ui)

        btn1.pack(pady=5)
        btn2.pack(pady=5)
        btn3.pack(pady=5)
        btn4.pack(pady=5)
        btn5.pack(pady=5)
        btn6.pack(pady=5)

    def image_to_pdf_ui(self):
        img_files = filedialog.askopenfilenames(title="Select Images", filetypes=[("Images", "*.jpg *.png *.jpeg")])
        if not img_files: return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not save_path: return
        try:
            image_to_pdf.images_to_pdf(img_files, save_path)
            messagebox.showinfo("Success", f"PDF saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def merge_pdf_ui(self):
        pdf_files = filedialog.askopenfilenames(title="Select PDFs to Merge", filetypes=[("PDF", "*.pdf")])
        if not pdf_files: return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not save_path: return
        try:
            merge_split_pdf.merge_pdfs(pdf_files, save_path)
            messagebox.showinfo("Success", f"PDF saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def split_pdf_ui(self):
        pdf_file = filedialog.askopenfilename(title="Select PDF to Split", filetypes=[("PDF", "*.pdf")])
        if not pdf_file: return
        page_range = simpledialog.askstring("Input", "Enter page range to extract (e.g., 1-3):")
        if not page_range: return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not save_path: return
        try:
            start, end = map(int, page_range.split('-'))
            merge_split_pdf.split_pdf(pdf_file, save_path, start, end)
            messagebox.showinfo("Success", f"Split PDF saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ocr_ui(self):
        pdf_file = filedialog.askopenfilename(title="Select PDF for OCR", filetypes=[("PDF", "*.pdf")])
        if not pdf_file: return
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt")])
        if not save_path: return
        try:
            text = ocr_extractor.ocr_pdf(pdf_file)
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(text)
            messagebox.showinfo("Success", f"Text extracted to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def compress_pdf_ui(self):
        pdf_file = filedialog.askopenfilename(title="Select PDF to Compress", filetypes=[("PDF", "*.pdf")])
        if not pdf_file: return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not save_path: return
        try:
            compressor.compress_pdf(pdf_file, save_path)
            messagebox.showinfo("Success", f"Compressed PDF saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def security_ui(self):
        win = tk.Toplevel(self.root)
        win.title("PDF Security")
        tk.Button(win, text="Add Password", command=self.add_password_ui).pack(fill='x')
        tk.Button(win, text="Remove Password", command=self.remove_password_ui).pack(fill='x')
        tk.Button(win, text="Add Watermark", command=self.add_watermark_ui).pack(fill='x')
        tk.Button(win, text="Add Signature", command=self.add_signature_ui).pack(fill='x')

    def add_password_ui(self):
        pdf_file = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF", "*.pdf")])
        if not pdf_file: return
        password = simpledialog.askstring("Password", "Enter password to set:")
        if not password: return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not save_path: return
        try:
            security.add_password(pdf_file, save_path, password)
            messagebox.showinfo("Success", f"Password set and saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def remove_password_ui(self):
        pdf_file = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF", "*.pdf")])
        if not pdf_file: return
        password = simpledialog.askstring("Password", "Enter current password:")
        if not password: return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not save_path: return
        try:
            security.remove_password(pdf_file, save_path, password)
            messagebox.showinfo("Success", f"Password removed, saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_watermark_ui(self):
        pdf_file = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF", "*.pdf")])
        if not pdf_file: return
        watermark_file = filedialog.askopenfilename(title="Select Watermark PDF", filetypes=[("PDF", "*.pdf")])
        if not watermark_file: return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not save_path: return
        try:
            security.add_watermark(pdf_file, watermark_file, save_path)
            messagebox.showinfo("Success", f"Watermarked PDF saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_signature_ui(self):
        pdf_file = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF", "*.pdf")])
        if not pdf_file: return
        signature_img = filedialog.askopenfilename(title="Select Signature Image", filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if not signature_img: return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not save_path: return
        try:
            security.add_signature(pdf_file, signature_img, save_path)
            messagebox.showinfo("Success", f"Signed PDF saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFAssistantApp(root)
    root.mainloop()
