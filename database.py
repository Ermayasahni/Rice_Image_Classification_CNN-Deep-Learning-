import mysql.connector as mysql

def get_conn():
    return mysql.connect(
        host = "localhost",
        user = "root",
        password = "maya1724"
    )
    
def create_db():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS RICE_IMAGE_DB")
    conn.close()
    

def create_table():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("USE RICE_IMAGE_DB")
    cursor.execute("""CREATE TABLE rice_predictions (
                     id INTEGER PRIMARY KEY AUTO_INCREMENT,
                     rice_type TEXT NOT NULL,
                     image_name TEXT NOT NULL,
                     prediction_time DATETIME DEFAULT CURRENT_TIMESTAMP
                     )
                   """)
    conn.close()
    

def save_prediction(rice_type, image_name):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("USE RICE_IMAGE_DB")

    cursor.execute("""
                    INSERT INTO rice_predictions (rice_type, image_name)
                    VALUES (%s, %s)
                   """, (rice_type, image_name))

    conn.commit()

def get_predictions():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("USE RICE_IMAGE_DB")

    cursor.execute("""
        SELECT id, rice_type, image_name, prediction_time
        FROM rice_predictions
        ORDER BY prediction_time DESC
    """)

    data = cursor.fetchall()

    conn.close()
    return data


