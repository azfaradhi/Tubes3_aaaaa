class BoyerMoore:
    def __init__(self):
        self.text = ""

    def set_text(self, text: str):
        self.text = text if text else ""

    def preprocess_bad_char(self, pattern: str):
        bad_char_table = {}
        for i in range(len(pattern)):
            bad_char_table[pattern[i]] = i
        return bad_char_table

    def bad_char_shift(self, bad_char_table, mismatched_char, mismatch_position):
        if mismatched_char in bad_char_table:
            return max(1, mismatch_position - bad_char_table[mismatched_char])
        return mismatch_position + 1

    def good_suffix_shift(self, pattern: str, mismatch_pos: int):
        pat_len = len(pattern)

        if mismatch_pos == pat_len - 1:
            return 1

        suffix_len = pat_len - mismatch_pos - 1
        suffix = pattern[mismatch_pos + 1:]

        for shift_start in range(mismatch_pos - suffix_len, -1, -1):
            if pattern[shift_start:shift_start + suffix_len] == suffix:
                return mismatch_pos - shift_start + 1

        for prefix_len in range(suffix_len - 1, 0, -1):
            if pattern[:prefix_len] == suffix[-prefix_len:]:
                return pat_len - prefix_len

        return pat_len

    def boyer_moore_algorithm(self, pattern: str):
        if not self.text or not pattern:
            return []

        found_positions = []
        text_length = len(self.text)
        pattern_length = len(pattern)
        bad_char_table = self.preprocess_bad_char(pattern)

        if pattern_length > text_length:
            return found_positions

        text_position = 0
        while text_position <= text_length - pattern_length:
            pattern_position = pattern_length - 1

            while pattern_position >= 0 and pattern[pattern_position] == self.text[text_position + pattern_position]:
                pattern_position -= 1

            if pattern_position < 0:
                found_positions.append(text_position)
                text_position += 1
            else:
                bad_char_shift_amt = self.bad_char_shift(bad_char_table, self.text[text_position + pattern_position], pattern_position)
                good_suffix_shift_amt = self.good_suffix_shift(pattern, pattern_position)
                text_position += max(bad_char_shift_amt, good_suffix_shift_amt)

        return found_positions
    
    def find_multiple_keywords_bm(self, keywords_str: str):
    
            # 1. Pisahkan string input menjadi daftar keyword yang bersih.
            keywords = [keyword.strip() for keyword in keywords_str.split(',')]
            
            # Inisialisasi dictionary untuk menyimpan hasil
            keyword_counts = {}

            # 2. Loop untuk setiap keyword dalam daftar
            for keyword in keywords:
                if not keyword:  # Lewati keyword kosong
                    continue
                
                # 3. Panggil algoritma Boyer-Moore yang sudah ada untuk satu keyword
                match_indices = self.boyer_moore_algorithm(keyword)
                
                # 4. Hitung jumlah hasil (panjang dari list) dan simpan
                keyword_counts[keyword] = len(match_indices)
                
            return keyword_counts