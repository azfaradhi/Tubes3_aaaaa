import mysql.connector
from mysql.connector import Error

def connect():
    try:
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
