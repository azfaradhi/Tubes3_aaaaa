class ProfileEncryption:
    def __init__(self, key: str):
        self.key = key
        self.blocks = []

    def _make_hash(self, text: str):
        hash_num = 0
        for i, char in enumerate(text):
            hash_num += ord(char) * (i + 1)
        return hash_num % 1000  

    def _make_block(self, char: str, prev_hash: int) -> dict:
        current_hash = self._make_hash(char + str(prev_hash))
        
        block = {
            'data': char,           
            'prev_hash': prev_hash, 
            'hash': current_hash    
        }
        return block

    def encrypt(self, text: str) -> str:
        if not text:
            return ""
        
        self.blocks = []
        encrypted_chars = []
        prev_hash = 0
        
        for i, char in enumerate(text):
            
            block = self._make_block(char, prev_hash)
            self.blocks.append(block)
            
            
            key_char = self.key[i % len(self.key)]  
            
            
            encrypted_ascii = ord(char) + ord(key_char) + block['hash']
            encrypted_ascii = encrypted_ascii % 95 + 32  
            
            encrypted_chars.append(chr(encrypted_ascii))
            prev_hash = block['hash']
        
        
        total_hash = sum(block['hash'] for block in self.blocks) % 1000
        signature = f"{total_hash:03d}"  
        
        return ''.join(encrypted_chars) + signature

    def decrypt(self, encrypted_text: str):
        if len(encrypted_text) < 3:
            return ""
        
        
        signature = encrypted_text[-3:]  
        data = encrypted_text[:-3]
        
        try:
            expected_total = int(signature)
        except:
            return ""
        
        
        self.blocks = []
        decrypted_chars = []
        prev_hash = 0
        
        for i, encrypted_char in enumerate(data):
            
            for test_ascii in range(32, 127):  
                test_char = chr(test_ascii)
                
                
                test_block = self._make_block(test_char, prev_hash)
                
                
                key_char = self.key[i % len(self.key)]
                expected_encrypted = ord(test_char) + ord(key_char) + test_block['hash']
                expected_encrypted = expected_encrypted % 95 + 32
                
                if chr(expected_encrypted) == encrypted_char:
                    
                    self.blocks.append(test_block)
                    decrypted_chars.append(test_char)
                    prev_hash = test_block['hash']
                    break
            else:
                
                return ""
        
        
        actual_total = sum(block['hash'] for block in self.blocks) % 1000
        
        if actual_total == expected_total:
            return ''.join(decrypted_chars)
        else:
            return ""  

if __name__ == "__main__":
    key = "ABCljfoihrouepoq"
    crypto = ProfileEncryption(key)
    text = "Hello"
    print(f"Original: {text}")
    encrypted = crypto.encrypt(text)
    print(f"Encrypted: {encrypted}")
    decrypted = crypto.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")