import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

# --- IMAGE TO PDF MODULE ---
from PIL import Image
def images_to_pdf(image_paths, output_pdf_path):
    images = [Image.open(img).convert('RGB') for img in image_paths]
    if not images:
        raise ValueError("No images provided")
    images[0].save(output_pdf_path, save_all=True, append_images=images[1:])
    return output_pdf_path

# --- PDF MERGE/SPLIT MODULE ---
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

# --- OCR EXTRACTOR MODULE ---
import pytesseract
from pdfplumber import open as pdfplumber_open
import io
def ocr_pdf(pdf_path):
    text = ""
    with pdfplumber_open(pdf_path) as pdf:
        for page in pdf.pages:
            # OCR on rasterized page
            img = page.to_image(resolution=300)
            img_buf = io.BytesIO()
            img.original.save(img_buf, format="PNG")
            img_buf.seek(0)
            image = Image.open(img_buf)
            text += pytesseract.image_to_string(image)
            # Also extract text via PDF if available
            extracted = page.extract_text()
            if extracted:
                text += "\n" + extracted
    return text

# --- SECURITY MODULE ---
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
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

# --- TOOLTIP UTILITY ---
class ToolTip(object):
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert") or (0, 0, 0, 0)
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#222", foreground="#fff", relief=tk.SOLID, borderwidth=1,
                         font=("Segoe UI", "10", "normal"))
        label.pack(ipadx=8, ipady=3)

    def leave(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

# --- MAIN APPLICATION GUI (ENHANCED APPEAL) ---
class PDFAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Assistant")
        self.root.geometry("450x500")
        self.root.configure(bg="#232946")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", font=("Segoe UI", 13), padding=6)
        
        # App Title
        title = tk.Label(root, text="PDF Assistant", font=("Segoe UI", 28, "bold"), bg="#232946", fg="#eebbc3")
        title.pack(pady=(28, 8))

        # Subtitle
        subtitle = tk.Label(root, text="All your PDF tools in one place", font=("Segoe UI", 12), bg="#232946", fg="#b8c1ec")
        subtitle.pack(pady=(0, 18))

        # Action frames
        action_frame = tk.Frame(root, bg="#232946")
        action_frame.pack(pady=(0, 20))

        btn1 = ttk.Button(action_frame, text="Image(s) to PDF", command=self.image_to_pdf_ui)
        btn2 = ttk.Button(action_frame, text="Merge PDFs", command=self.merge_pdf_ui)
        btn3 = ttk.Button(action_frame, text="Split PDF", command=self.split_pdf_ui)
        btn4 = ttk.Button(action_frame, text="Extract Text (OCR)", command=self.ocr_ui)
        btn5 = ttk.Button(action_frame, text="PDF Security", command=self.security_ui)

        # Pack with spacing
        for i, (btn, tip) in enumerate([
            (btn1, "Convert images to a single PDF"),
            (btn2, "Merge multiple PDF files into one"),
            (btn3, "Extract selected pages from a PDF"),
            (btn4, "Extract text from PDF using OCR"),
            (btn5, "Add/remove password, watermark, or signature")
        ]):
            btn.pack(fill="x", pady=6, padx=25)
            ToolTip(btn, tip)
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.configure(style="Hover.TButton"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(style="TButton"))

        # Style for hover
        self.style.map("Hover.TButton",
            background=[('active', '#eebbc3')],
            foreground=[('active', '#232946')]
        )

        # Footer
        footer = tk.Label(root, text="© 2025 PDF Assistant", font=("Segoe UI", 8), bg="#232946", fg="#b8c1ec")
        footer.pack(side="bottom", pady=8)

    def image_to_pdf_ui(self):
        img_files = filedialog.askopenfilenames(title="Select Images", filetypes=[("Images", "*.jpg *.png *.jpeg *.bmp")])
        if not img_files: return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not save_path: return
        try:
            images_to_pdf(img_files, save_path)
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
            merge_pdfs(pdf_files, save_path)
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
            split_pdf(pdf_file, save_path, start, end)
            messagebox.showinfo("Success", f"Split PDF saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ocr_ui(self):
        pdf_file = filedialog.askopenfilename(title="Select PDF for OCR", filetypes=[("PDF", "*.pdf")])
        if not pdf_file: return
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt")])
        if not save_path: return
        try:
            text = ocr_pdf(pdf_file)
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(text)
            messagebox.showinfo("Success", f"Text extracted to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def security_ui(self):
        win = tk.Toplevel(self.root)
        win.title("PDF Security")
        win.configure(bg="#232946")
        win.geometry("340x290")
        sec_label = tk.Label(win, text="PDF Security Tools", font=("Segoe UI", 16, "bold"), bg="#232946", fg="#eebbc3")
        sec_label.pack(pady=(22, 14))

        for text, cmd, tip in [
            ("Add Password", self.add_password_ui, "Set a password for a PDF"),
            ("Remove Password", self.remove_password_ui, "Remove a password from a PDF"),
            ("Add Watermark", self.add_watermark_ui, "Overlay a watermark on PDF"),
            ("Add Signature", self.add_signature_ui, "Digitally sign a PDF with an image")
        ]:
            btn = ttk.Button(win, text=text, command=cmd)
            btn.pack(fill="x", pady=7, padx=28)
            ToolTip(btn, tip)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(style="Hover.TButton"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(style="TButton"))

    def add_password_ui(self):
        pdf_file = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF", "*.pdf")])
        if not pdf_file: return
        password = simpledialog.askstring("Password", "Enter password to set:")
        if not password: return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not save_path: return
        try:
            add_password(pdf_file, save_path, password)
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
            remove_password(pdf_file, save_path, password)
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
            add_watermark(pdf_file, watermark_file, save_path)
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
            add_signature(pdf_file, signature_img, save_path)
            messagebox.showinfo("Success", f"Signed PDF saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFAssistantApp(root)
    root.mainloop()