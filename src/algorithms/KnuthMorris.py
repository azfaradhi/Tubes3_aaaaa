class KnuthMorris:

    def __init__(self):
        self.text = ""

    def set_text(self, text: str):
        self.text = text if text else ""
    
    def identify_border_table(self, pattern: str):
        lsp = [0] * len(pattern)
        length = 0
        i = 1

        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lsp[i] = length
                i += 1
            else:
                if length != 0:
                    length = lsp[length - 1]
                else:
                    lsp[i] = 0
                    i += 1
                    
        return lsp
    
    def kmp_algorithm(self, pattern: str):
        if not self.text or not pattern:
            return []

        lsp = self.identify_border_table(pattern)
        result_index = []

        i = 0
        j = 0

        while i < len(self.text):
            if pattern[j] == self.text[i]:
                i += 1
                j += 1

            if j == len(pattern):
                result_index.append(i - j)
                j = lsp[j - 1]
            elif i < len(self.text) and pattern[j] != self.text[i]:
                if j != 0:
                    j = lsp[j - 1]
                else:
                    i += 1

        return result_index

    def find_multiple_keywords_kmp(self, keywords_str: str):
            keywords = [keyword.strip() for keyword in keywords_str.split(',')]
            
            keyword_counts = {}

            for keyword in keywords:
                if not keyword:
                    continue
                match_indices = self.kmp_algorithm(keyword)
                
                keyword_counts[keyword] = len(match_indices)
                
            return keyword_counts