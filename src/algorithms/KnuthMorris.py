
# cara pemakaian: inisialisasi class KnuthMorris dengan
# parameter pattern yang akan dicocokan

# untuk setiap text yang akan diidentifikasi, parsing di fungsi kmp_algorithm
# return fungsi adalah list of index cocok

# perlu penyesuaian di tempat lain terkait path file terkait

class KnuthMorris:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.lsp = [0] * len(pattern)
        self.identify_border_table()
    
    def identify_border_table(self):
        if len(self.pattern) == 0:
            return []
        length = 0
        self.lsp[0] = 0
        i = 1

        while i < len(self.pattern):
            if self.pattern[i] == self.pattern[length]:
                length += 1
                self.lsp[i] = length
                i += 1
            else:
                if length != 0:
                    length = self.lsp[length - 1]
                else:
                    self.lsp[i] = 0
                    i += 1
    
    def kmp_algorithm(self, text: str):
        result_index = []
        n = len(text)
        m = len(self.pattern)
        i = 0
        j = 0
        while (i < n):
            if (self.pattern[j] == text[i]):
                i += 1
                j += 1

            if (j == m):
                result_index.append(i - j)
                j = self.lsp[j-1]
            else:
                if ((i < n) and self.pattern[j] != text[i]):
                    if (j != 0):
                        j = self.lsp[j-1]
                    else:
                        i += 1
        return result_index

# contoh pemakaian:
# kmp = KnuthMorris("abc")
# print(kmp.kmp_algorithm("abcabcabc"))  # Output: [0, 3, 6]