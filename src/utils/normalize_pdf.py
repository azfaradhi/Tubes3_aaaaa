import os
import fitz
import re

class PDFTextConverter:
    def __init__(self):
        self.pdf_path = ""

    def set_pdf_path(self, pdf_path):
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file {pdf_path} does not exist.")
        self.pdf_path = pdf_path

    def to_text_raw(self, pdf_path: str) -> str:
        self.set_pdf_path(pdf_path)
        doc = fitz.open(self.pdf_path)
        full_text = ""
        for page in doc:
            text = page.get_text()
            full_text += text + "\n"
        doc.close()
        return full_text

    def to_text_normalized(self) -> str:
        doc = fitz.open(self.pdf_path)
        full_text = ""
        for page in doc:
            text = page.get_text()
            text = text.lower()
            text = re.sub(r'[^a-z0-9\s]', ' ', text)
            full_text += text.replace("\n", " ") + " "
        doc.close()

        full_text = ' '.join(full_text.split())
        return full_text