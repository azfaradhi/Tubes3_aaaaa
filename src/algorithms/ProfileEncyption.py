import re
import base64
import os
import mysql.connector
from mysql.connector import Error

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
        return {'data': char, 'prev_hash': prev_hash, 'hash': current_hash}

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
            encrypted_ascii = (ord(char) + ord(key_char) + block['hash']) % 95 + 32
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
        
def process_and_insert_data(sql_file_path: str, db_config: dict, encryption_key: str):
    print(f"Membaca file SQL dari: {sql_file_path}")
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            full_sql_content = f.read()
    except FileNotFoundError:
        print(f"Error: File tidak ditemukan di '{sql_file_path}'")
        return

    crypto = ProfileEncryption(encryption_key)
    
    connection = None
    try:
        print(f"Menghubungkan ke database '{db_config['database']}'...")
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        print("Menghapus data lama dari tabel...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE ApplicationDetail;")
        cursor.execute("TRUNCATE TABLE ApplicantProfile;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        print("Data lama berhasil dihapus.")

        profile_pattern = re.compile(r"INSERT INTO ApplicantProfile \(.*?\) VALUES\s*([\s\S]*?);", re.MULTILINE)
        profile_match = profile_pattern.search(full_sql_content)
        
        if profile_match:
            values_block = profile_match.group(1)
            row_pattern = re.compile(r"\(\s*(\d+),\s*'([^']*)',\s*'([^']*)',\s*'([^']*)',\s*'([^']*)',\s*'([^']*)'\s*\)")
            data_rows = row_pattern.findall(values_block)
            
            print(f"Memproses dan mengenkripsi data nama & alamat dari {len(data_rows)} baris...")

            insert_query = """
                INSERT INTO ApplicantProfile (applicant_id, first_name, last_name, date_of_birth, address, phone_number)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            for row in data_rows:
                applicant_id, first_name, last_name, dob, address, phone = row

                encrypted_fn = base64.b64encode(crypto.encrypt(first_name).encode('utf-8')).decode('utf-8')
                encrypted_ln = base64.b64encode(crypto.encrypt(last_name).encode('utf-8')).decode('utf-8')
                encrypted_addr = base64.b64encode(crypto.encrypt(address).encode('utf-8')).decode('utf-8')
                encrypted_phone = base64.b64encode(crypto.encrypt(phone).encode('utf-8')).decode('utf-8')

                original_dob = dob
                original_phone = phone

                cursor.execute(insert_query, (
                    applicant_id, 
                    encrypted_fn,
                    encrypted_ln, 
                    original_dob,
                    encrypted_addr,
                    encrypted_phone
                ))
            
            print("Data ApplicantProfile berhasil dimasukkan.")

        insert_application_details(cursor, full_sql_content)
        connection.commit()

    except Error as e:
        if connection:
            connection.rollback()
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Koneksi ke database ditutup.")

def insert_application_details(cursor, sql_content):
    detail_pattern = re.compile(
        r"INSERT INTO ApplicationDetail \(.*?\) VALUES\s*([\s\S]*?);", 
        re.MULTILINE
    )
    detail_match = detail_pattern.search(sql_content)
    
    if not detail_match:
        print("Peringatan: Tidak dapat menemukan blok 'INSERT INTO ApplicationDetail'.")
        return

    values_block = detail_match.group(1)
    row_pattern = re.compile(r"\(\s*(\d+),\s*(\d+),\s*(NULL|'[^']*'),\s*'([^']*)'\s*\)")
    data_rows = row_pattern.findall(values_block)
    
    print(f"Memasukkan {len(data_rows)} data ApplicationDetail...")

    insert_query = """
        INSERT INTO ApplicationDetail (detail_id, applicant_id, application_role, cv_path)
        VALUES (%s, %s, %s, %s)
    """

    for row in data_rows:
        detail_id, applicant_id, role, cv_path = row
        
        if role.upper() == 'NULL':
            application_role = None
        else:
            application_role = role.strip("'")
            
        data_to_insert = (detail_id, applicant_id, application_role, cv_path)
        cursor.execute(insert_query, data_to_insert)

    print("Data ApplicationDetail berhasil dimasukkan.")

if __name__ == "__main__":
    input_sql_file = 'tubes3_seeding.sql'
    
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "radhi",
        "database": "cv_ats"
    }
    
    MY_SECRET_KEY = "kumalalasavesta"

    process_and_insert_data(input_sql_file, db_config, MY_SECRET_KEY)
