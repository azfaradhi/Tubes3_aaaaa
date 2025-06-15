import os
import fitz
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import multiprocessing


class PDFTextConverter:
    def __init__(self, max_workers=None):
        self.pdf_path = ""
        # Default menggunakan jumlah CPU cores, tapi bisa di-set manual
        self.max_workers = max_workers or min(32, multiprocessing.cpu_count() + 4)
        self.text_lock = Lock()

    def set_pdf_path(self, pdf_path):
        if not os.path.exists(pdf_path):
            print(f"PDF file {pdf_path} does not exist.")
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

    def _process_page(self, page_data):
        page_num, pdf_path = page_data
        doc = fitz.open(pdf_path)
        page = doc[page_num]
        text = page.get_text()
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        normalized_text = text.replace("\n", " ")
        
        doc.close()
        return page_num, normalized_text

    def to_text_normalized_multithread(self) -> str:
        if not self.pdf_path:
            raise ValueError("PDF path tidak di-set.")
        doc = fitz.open(self.pdf_path)
        total_pages = len(doc)
        doc.close()
        
        page_data = [(page_num, self.pdf_path) for page_num in range(total_pages)]
        
        page_results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_page = {
                executor.submit(self._process_page, data): data[0] 
                for data in page_data
            }
            
            for future in as_completed(future_to_page):
                try:
                    page_num, normalized_text = future.result()
                    page_results[page_num] = normalized_text
                except Exception as e:
                    print(f"Error processing page {future_to_page[future]}: {e}")
                    page_results[future_to_page[future]] = ""
        
        full_text = ""
        for page_num in sorted(page_results.keys()):
            full_text += page_results[page_num] + " "
        
        full_text = ' '.join(full_text.split())
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
    
# if __name__ == "__main__":
#     pdf_converter = PDFTextConverter(max_workers=8)
#     pdf_converter.set_pdf_path("data/ACCOUNTANT/10554236.pdf")
#     print(pdf_converter.to_text_raw("data/ACCOUNTANT/10554236.pdf"))