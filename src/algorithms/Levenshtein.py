
class Levenshtein:

    def __init__(self,):
        self.text = ""
    
    def setText(self, text):
        self.text = text

    def levenshteinFullMatrix(str1, str2):
        m = len(str1)
        n = len(str2)

        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i - 1] == str2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1])
        return dp[m][n]
    
    def distance(str1, str2):
        return Levenshtein.levenshteinFullMatrix(str1, str2)
    
    def similarity(self, str1, str2):
        if not str1 and not str2:
            return 1.0
        if not str1 or not str2:
            return 0.0
        max_len = max(len(str1), len(str2))
        return 1 - (Levenshtein.distance(str1, str2) / max_len)

    # str1 text yang menjadi pembanding (pattern)
    # str2 text panjang yang akan dibandingkan
    # return adalah list index dan panjang kata yang persentasenya di atas threshold
    @staticmethod
    def fuzzy_compare(str1, str2, threshold):

        if not str1 or not str2:
            return []
        
        pattern = str1.lower().strip()
        text = str2.lower().strip()
        
        matches = []
        
        if len(pattern) >= len(text):
            max_len = max(len(pattern), len(text))
            distance = Levenshtein.distance(pattern, text)
            similarity = 1 - (distance / max_len)
            if similarity >= threshold:
                matches.append({
                    'start': 0,
                    'length': len(text),
                    'similarity': similarity
                })
            return matches
        
        pattern_len = len(pattern)
        
        for i in range(len(text) - pattern_len + 1):
            substring = text[i:i + pattern_len]
            
            if substring == pattern:
                continue
                
            distance = Levenshtein.distance(pattern, substring)
            similarity = 1 - (distance / pattern_len)
            
            if similarity >= threshold:
                matches.append({
                    'start': i,
                    'length': pattern_len,
                    'similarity': similarity
                })
        
        extended_window = int(pattern_len * 1.2)
        if extended_window <= len(text):
            for i in range(len(text) - extended_window + 1):
                substring = text[i:i + extended_window]
                
                if pattern in substring or substring in pattern:
                    continue
                    
                distance = Levenshtein.distance(pattern, substring)
                similarity = 1 - (distance / max(len(pattern), len(substring)))
                
                if similarity >= threshold:
                    is_duplicate = False
                    for j, match in enumerate(matches):
                        if (i < match['start'] + match['length'] and i + extended_window > match['start']):
                            if similarity > match['similarity']:
                                matches[j] = {
                                    'start': i,
                                    'length': extended_window,
                                    'similarity': similarity
                                }
                            is_duplicate = True
                            break
                    
                    if not is_duplicate:
                        matches.append({
                            'start': i,
                            'length': extended_window,
                            'similarity': similarity
                        })
        
        matches.sort(key=lambda x: x['similarity'], reverse=True)
        return matches

    @staticmethod
    def search_levenhstein(str1, str2):
        results = Levenshtein.fuzzy_compare(str1, str2, 0.75)
        return [{
            'start': match['start'],
            'length': match['length'],
            'similarity': int(match['similarity'] * 100)
        } for match in results]
    
    def search_levenhstein_from_long_string(self, str1, threshold=0.75):
        if not str1 or not self.text:
            return []

        str1 = str1.lower().strip()

        pattern_len = len(str1)
        matches = []

        window_range = range(max(1, pattern_len - 3), pattern_len + 4)
        text_len = len(self.text)

        for window_size in window_range:
            for i in range(text_len - window_size + 1):
                substring = self.text[i:i + window_size]

                if substring == str1:
                    continue

                distance = Levenshtein.distance(str1, substring)
                similarity = 1 - (distance / max(len(substring), pattern_len))

                if similarity >= threshold:
                    is_duplicate = False
                    for j, match in enumerate(matches):
                        if (i < match['start'] + match['length'] and i + window_size > match['start']):
                            if similarity > match['similarity']:
                                matches[j] = {
                                    'start': i,
                                    'length': window_size,
                                    'similarity': similarity
                                }
                            is_duplicate = True
                            break

                    if not is_duplicate:
                        matches.append({
                            'start': i,
                            'length': window_size,
                            'similarity': similarity
                        })

        matches.sort(key=lambda x: x['similarity'], reverse=True)

        return [{
            'start': m['start'],
            'length': m['length'],
            'similarity': round(m['similarity'] * 100, 2),
            'match_text': self.text[m['start']:m['start'] + m['length']]
        } for m in matches]
    
    def find_multiple_keywords_fuzzy(self, keywords_str: str, threshold=0.75):
        keywords = [keyword.strip() for keyword in keywords_str.split(',')]
        
        keyword_counts = {}

        for keyword in keywords:
            if not keyword:
                continue
            
            fuzzy_matches = self.search_levenhstein_from_long_string(
                keyword, threshold
            )
            
            if fuzzy_matches:
                keyword_counts[keyword] = len(fuzzy_matches)
                
        return keyword_counts