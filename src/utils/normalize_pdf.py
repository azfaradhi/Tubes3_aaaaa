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

    # regex pake ini(?)
    def to_text_raw(self, pdf_path: str) -> str:
        self.set_pdf_path(pdf_path)
        doc = fitz.open(self.pdf_path)
        full_text = ""
        for page in doc:
            text = page.get_text()
            full_text += text + "\n"
        doc.close()
        return full_text

    #string matching pake ini yeah
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

# if __name__ == "__main__":
#     converter = PDFTextConverter()
#     pdf_file_path = "data/ACCOUNTANT/10554236.pdf"
#     try:
#         converter.set_pdf_path(pdf_file_path)
#         text_raw = converter.to_text_normalized()
#         print("Raw Text Extracted:")
#         print(text_raw)

#     except FileNotFoundError as e:
#         print(e)