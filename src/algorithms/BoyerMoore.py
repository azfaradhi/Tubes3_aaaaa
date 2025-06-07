class BoyerMoore:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.pattern_length = len(pattern)
        self.bad_char_table = {}
        for i in range(self.pattern_length):
            self.bad_char_table[self.pattern[i]] = i
    
    # menari kemunculan terakhir karakter di sebelah kiri posisi mismatch
    def bad_char_shift(self, mismatched_char, mismatch_position):
        if mismatched_char in self.bad_char_table:
            return max(1, mismatch_position - self.bad_char_table[mismatched_char])
        return mismatch_position + 1
    
    def good_suffix_shift(self, mismatch_pos):
        pat_len = self.pattern_length

        # Jika mismatch di posisi terakhir (artinya suffix kosong), geser 1
        if mismatch_pos == pat_len - 1:
            return 1

        suffix_len = pat_len - mismatch_pos - 1
        suffix = self.pattern[mismatch_pos + 1 :]

        for shift_start in range(mismatch_pos-suffix_len, -1, -1):
            if self.pattern[shift_start:shift_start + suffix_len] == suffix:
                return mismatch_pos - shift_start + 1

        # kalo gaada suffix yang sama, cek partial match dengan prefix
        for prefix_len in range(suffix_len - 1, 0, -1):
            if self.pattern[:prefix_len] == suffix[-prefix_len:]:
                return pat_len - prefix_len

        return pat_len # Jika tidak ada yang cocok, geser sesuai panjang pattern
            
    def search(self, text: str):
        found_positions = []
        text_length = len(text)
        
        if self.pattern_length > text_length:
            return found_positions
        
        text_position = 0
        while text_position <= text_length - self.pattern_length:
            pattern_position = self.pattern_length - 1
            
            # Cocokkan dari kanan ke kiri
            while pattern_position >= 0 and self.pattern[pattern_position] == text[text_position + pattern_position]:
                pattern_position -= 1
            
            if pattern_position < 0:
                # Pattern ditemukan
                found_positions.append(text_position)
                text_position += 1
            else:
                # Hitung pergeseran menggunakan kedua rule
                bad_char_shift_amount = self.bad_char_shift(text[text_position + pattern_position], pattern_position)
                good_suffix_shift_amount = self.good_suffix_shift(pattern_position)
                text_position += max(bad_char_shift_amount, good_suffix_shift_amount)
        
        return found_positions



# Contoh penggunaan:
if __name__ == "__main__":
    bm = BoyerMoore("international")
    text = "internationalede"
    print(bm.search(text))