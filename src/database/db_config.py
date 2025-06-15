import mysql.connector
from mysql.connector import Error

def connect():
    try:
        # harusnya pakai env tapi biarin dah
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="radhi",
            database="cv_ats",
        )
        if conn.is_connected():
            return conn
        else:
            return None
    except Error as e:
        return None
