import sqlite3
from datetime import datetime

DB_NAME = "chatbot.db"

def create_connection():
    try:
        connection = sqlite3.connect(DB_NAME)
        connection.row_factory = sqlite3.Row
        return connection
    except Exception as e:
        print(f"Error creating connection: {str(e)}")
        return None
    
def create_app_logs():
    connection = create_connection()
    try:
        connection.execute('''CREATE TABLE IF NOT EXISTS application_logs
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            session_id TEXT,
                            query TEXT,
                            response TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        connection.close()
    except Exception as e:
        print(f"Error creating application_logs table: {str(e)}")