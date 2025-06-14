from database.db_config import *

class db_search:
    def __init__(self, conn):
        self.db_config = conn

    def get_connection(self):
        return self.db_config
    def getAllName(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT applicant_id, first_name, last_name FROM ApplicantProfile")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    def getNameByApplicantId(self, applicant_id: int):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT first_name, last_name FROM ApplicantProfile WHERE applicant_id = %s", (applicant_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def getAllDateOfBirth(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT applicant_id, date_of_birth FROM ApplicantProfile")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    
    def getAllPhoneNumber(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT applicant_id, phone_number FROM ApplicantProfile")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    def getPhoneNumberByApplicantId(self, applicant_id: int):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT phone_number FROM ApplicantProfile WHERE applicant_id = %s", (applicant_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    
    def getAllApplicationDetails(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT ad.*, ap.applicant_id 
        FROM ApplicationDetail ad
        JOIN ApplicantProfile ap ON ad.applicant_id = ap.applicant_id
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    def getApplicationDetailById(self, applicant_id: int):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT ap.*, ad.role, ad.cv_path 
        FROM ApplicantProfile ap
        JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id
        WHERE ap.applicant_id = %s
        """
        cursor.execute(query, (applicant_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result