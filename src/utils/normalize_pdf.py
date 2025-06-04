import os
import fitz
import re

class PDFTextConverter:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def to_text_raw(self, txt_output_path):
        doc = fitz.open(self.pdf_path)
        os.makedirs(os.path.dirname(txt_output_path), exist_ok=True)
        with open(txt_output_path, "w", encoding="utf-8") as f:
            for page in doc:
                text = page.get_text()
                f.write(text + "\n")
        doc.close()
        print(f"{self.pdf_path} -> {txt_output_path} (raw)")

    def to_text_normalized(self, txt_output_path):
        doc = fitz.open(self.pdf_path)
        full_text = ""
        for page in doc:
            text = page.get_text()
            text = text.lower()
            text = re.sub(r'[^a-z0-9\s]', ' ', text)
            full_text += text.replace("\n", " ") + " "
        doc.close()

        full_text = ' '.join(full_text.split())

        os.makedirs(os.path.dirname(txt_output_path), exist_ok=True)
        with open(txt_output_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        print(f"{self.pdf_path} -> {txt_output_path} (normalized)")

# def convert_all_pdfs_in_folder(root_folder, output_root):
#     for dirpath, dirnames, filenames in os.walk(root_folder):
#         for filename in filenames:
#             if filename.lower().endswith(".pdf"):
#                 pdf_path = os.path.join(dirpath, filename)
#                 relative_path = os.path.relpath(pdf_path, root_folder)

#                 raw_output_path = os.path.join(output_root, "raw", os.path.splitext(relative_path)[0] + ".txt")
#                 normalized_output_path = os.path.join(output_root, "normalized", os.path.splitext(relative_path)[0] + ".txt")

#                 converter = PDFTextConverter(pdf_path)
#                 converter.to_text_raw(raw_output_path)
#                 converter.to_text_normalized(normalized_output_path)

# if __name__ == "__main__":
#     input_folder = "data"
#     output_folder = "text"
#     convert_all_pdfs_in_folder(input_folder, output_folder)
