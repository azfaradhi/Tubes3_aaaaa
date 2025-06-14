import json.scanner
from src.database.db_search import *
from src.algorithms.KnuthMorris import *
from src.algorithms.Levenshtein import *
from src.algorithms.BoyerMoore import *
from src.algorithms.AhoCorasick import *
from src.algorithms.ProfileEncyption import *
from src.utils.normalize_pdf import *
import json

from src.algorithms.Regex import Regex

class Controller:

    allData = []
    def __init__(self,conn):
        self.pdf = PDFTextConverter()
        self.kmp = KnuthMorris()
        self.booye = BoyerMoore()
        self.aho = AhoCorasick("APA")
        self.search = db_search(conn)
        Controller.allData = self.search.getAllData()
        self.crypto = ProfileEncryption("kumalalasavesta")
        self.decryptProfile(self.crypto)
        self.mapPathAndData = {}
        self.preProcessText()

    def decrypt_safe(self,cipher_text_base64, cipher):
        try:
            raw_cipher = base64.b64decode(cipher_text_base64).decode('latin1')
            return cipher.decrypt(raw_cipher)
        except Exception as e:
            print(f"[ERROR decoding/decrypting] {e}")
            return ""
        
    def decryptProfile(self, cipher):
        for data in self.allData:
            for field in ["first_name", "last_name", "phone_number", "address"]:
                encrypted = data[field]
                decrypted = self.decrypt_safe(encrypted, cipher)
                if decrypted == "":
                    print(f"[Decrypt failed] {field}: {encrypted}")
                data[field] = decrypted

        
    @staticmethod
    def getDataByIndex(index: int):
        if 0 <= index < len(Controller.allData):
            return Controller.allData[index]
    
    def preProcessText(self):
        for i, data in enumerate(self.allData):
            if (i < 10):
                path = data.get('cv_path', '')
                if path not in self.mapPathAndData:
                    self.pdf.set_pdf_path(path)
                    text = self.pdf.to_text_normalized()
                    self.mapPathAndData[path] = text
                else:
                    text = self.mapPathAndData[path]
                print(f"Processing {i+1}/{len(self.allData)}: {path}")

    def searchQuery(self, pattern: str, algorithm: str, max: int):
        results = {}
        for i, data in enumerate(self.allData):
            if i < 10:
                path = data.get('cv_path', '')
                document_text = self.mapPathAndData.get(path, '')
                if algorithm == 'kmp':
                    self.kmp.set_text(document_text)
                    foundedList = self.kmp.find_multiple_keywords_kmp(pattern.lower())
                elif algorithm == 'booye':
                    self.booye.set_text(document_text)
                    foundedList = self.booye.find_multiple_keywords_bm(pattern.lower())
                elif algorithm == 'aho':
                    self.aho.set_pattern(pattern.lower())
                    foundedList = self.aho.search(document_text)

                if foundedList:
                    results[i] = {
                        "applicant_id": data.get('applicant_id', ''),
                        "cv_path": path,
                        "name": f"{data.get('first_name', '')} {data.get('last_name', '')}",
                        "count": sum(foundedList.values()),
                        "keywords_count": foundedList
                    }

        if not results:
            print(f"Pattern '{pattern}' not found in any documents using KMP. Trying fuzzy matching...")
            for i, data in enumerate(self.allData):
                if i < 10:
                    path = data.get('cv_path', '')
                    document_text = self.mapPathAndData.get(path, '')
                    self.kmp.set_text(document_text)
                    foundedList = Levenshtein.find_multiple_keywords_fuzzy(pattern.lower(), document_text)

                    if foundedList:
                        results[i] = {
                            "applicant_id": data.get('applicant_id', ''),
                            "cv_path": path,
                            "name": f"{data.get('first_name', '')} {data.get('last_name', '')}",
                            "keywords_count": foundedList,
                            "count": len(foundedList)
                        }

        sorted_list = sorted(results.items(), key=lambda item: item[1]['count'], reverse=True)

        return dict(sorted_list[:max])
    
    def searchhh(self, text,pattern):
        self.kmp.set_text(text)
        return self.kmp.kmp_algorithm(pattern)
    
    @staticmethod
    def get_data(path: str):
        pdf_converter = PDFTextConverter(max_workers=8)
        pdf_converter.set_pdf_path(path)
        text = pdf_converter.to_text_raw(path)
        regex = Regex(text)
        experience = regex.extract_experience()
        education = regex.extract_education()
        skill = regex.extract_skills()
        return (experience, education, skill)
    
    