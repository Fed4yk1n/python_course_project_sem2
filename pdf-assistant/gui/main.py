import tkinter as tk
from tkinter import filedialog, messagebox
from modules import image_to_pdf, merge_split_pdf, ocr_extractor, security

class PDFApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Assistant")

        self.img2pdf_btn = tk.Button(self, text="Images to PDF", command=self.img2pdf_ui)
        self.img2pdf_btn.pack()

        self.merge_btn = tk.Button(self, text="Merge PDFs", command=self.merge_pdf_ui)
        self.merge_btn.pack()

        self.split_btn = tk.Button(self, text="Split PDF", command=self.split_pdf_ui)
        self.split_btn.pack()

        self.ocr_btn = tk.Button(self, text="OCR Extract", command=self.ocr_pdf_ui)
        self.ocr_btn.pack()

        self.security_btn = tk.Button(self, text="Add Password", command=self.add_password_ui)
        self.security_btn.pack()

    def img2pdf_ui(self):
        img_files = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
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
        if not pdf_files or len(pdf_files) < 2:
            messagebox.showerror("Error", "Please select at least two PDF files to merge.")
            return
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
        pages_str = tk.simpledialog.askstring("Pages", "Enter page numbers to extract (comma separated, 0-based):")
        if not pages_str: return
        try:
            pages = [int(x.strip()) for x in pages_str.split(",") if x.strip().isdigit()]
        except Exception:
            messagebox.showerror("Error", "Invalid page numbers.")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not save_path: return
        try:
            merge_split_pdf.split_pdf(pdf_file, pages, save_path)
            messagebox.showinfo("Success", f"PDF saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ocr_pdf_ui(self):
        pdf_file = filedialog.askopenfilename(title="Select PDF for OCR", filetypes=[("PDF", "*.pdf")])
        if not pdf_file: return
        try:
            text = ocr_extractor.ocr_pdf(pdf_file)
            save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if save_path:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(text)
                messagebox.showinfo("Success", f"OCR text saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_password_ui(self):
        pdf_file = filedialog.askopenfilename(title="Select PDF to Secure", filetypes=[("PDF", "*.pdf")])
        if not pdf_file: return
        password = tk.simpledialog.askstring("Password", "Enter password to set:", show="*")
        if not password: return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not save_path: return
        try:
            security.add_password(pdf_file, save_path, password)
            messagebox.showinfo("Success", f"Password protected PDF saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = PDFApp()
    app.mainloop()