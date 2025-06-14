import json.scanner
from database.db_search import *
from algorithms.KnuthMorris import *
from algorithms.Levenshtein import *
from algorithms.BoyerMoore import *
from algorithms.AhoCorasick import *
from utils.normalize_pdf import *
import json


class Controller:
    def __init__(self,conn):
        self.pdf = PDFTextConverter()
        self.kmp = KnuthMorris()
        self.booye = BoyerMoore()
        self.aho = AhoCorasick("APA")
        self.search = db_search(conn)
        self.allData = self.search.getAllData()
        self.mapPathAndData = {}
        self.preProcessText()
        print(f"Total applicants: {len(self.allData)}")

    def getDataByIndex(self, index: int):
        if 0 <= index < len(self.allData):
            return self.allData[index]
        
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

    def searchQuery(self, pattern: str, algorithm: str):
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
                        "count": len(foundedList),
                        "keywords_count": foundedList
                    }

        if not results:
            print(f"Pattern '{pattern}' not found in any documents using KMP. Trying fuzzy matching...")
            for i, data in enumerate(self.allData):
                if i < 10:
                    path = data.get('cv_path', '')
                    document_text = self.mapPathAndData.get(path, '')
                    self.kmp.set_text(document_text)
                    foundedList = Levenshtein.search_levenhstein_from_long_string(pattern.lower(), document_text)

                    if foundedList:
                        results[i] = {
                            "applicant_id": data.get('applicant_id', ''),
                            "count": len(foundedList)
                        }

        return results
    
    def searchhh(self, text,pattern):
        self.kmp.set_text(text)
        return self.kmp.kmp_algorithm(pattern)