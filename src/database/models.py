from db_config import get_connection

class ApplicantProfile:
    def __init__(self, id = None, first_name=None, last_name=None, date_of_birth=None, address=None, phone_number=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.phone_number = phone_number

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ApplicantProfile (applicant_id, first_name, last_name, date_of_birth, address, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (self.id, self.first_name, self.last_name, self.date_of_birth, self.address, self.phone_number))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def select_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ApplicantProfile")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows


class ApplicationDetail:
    def __init__(self, detail_id, applicant_id, role=None, cv_path=None):
        self.detail_id = detail_id
        self.applicant_id = applicant_id
        self.application_role = role
        self.cv_path = cv_path

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ApplicationDetail (detail_id, applicant_id, application_role, cv_path)
            VALUES (%s, %s, %s, %s)
        """, (self.detail_id, self.applicant_id, self.application_role, self.cv_path))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def select_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ApplicationDetail")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
