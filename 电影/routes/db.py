import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='',
        user='',
        password='',
        database=''
    )

def close_connection(conn):
    if conn.is_connected():
        conn.close()

