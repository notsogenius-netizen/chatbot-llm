import sqlite3
from datetime import datetime
import logging

DB_NAME = "chatbot.db"

def create_connection():
    try:
        connection = sqlite3.connect(DB_NAME)
        connection.row_factory = sqlite3.Row
        return connection
    except Exception as e:
        logging.error(f"Error creating connection: {str(e)}")
        return None
    
def create_app_logs():
    connection = create_connection()
    try:
        connection.execute('''CREATE TABLE IF NOT EXISTS app_logs
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            session_id TEXT,
                            query TEXT,
                            response TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        connection.close()
    except Exception as e:
        logging.error(f"Error creating application_logs table: {str(e)}")

def insert_app_logs(session_id, query, response):
    connection = create_connection()
    try:
        connection.execute('''INSERT INTO app_logs (session_id, query, response)
                            VALUES (?, ?, ?)''', (session_id, query, response))
        connection.commit()
        connection.close()
    except Exception as e:
        logging.error(f"Error inserting into application_logs: {str(e)}")

def get_chat_history(session_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT query, response FROM app_logs WHERE session_id = ? ORDER BY created_at', (session_id,))
    messages = []
    for row in cursor.fetchall():
        messages.extend([
            {"role": "human", "content": row['query']},
            {"role": "ai", "content": row['response']}
        ])
    conn.close()
    return messages

def create_document_store():
    connection = create_connection()
    try:
        connection.execute('''CREATE TABLE IF NOT EXISTS document_store
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            filename TEXT,
                            upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        connection.close()
    except Exception as e:
        logging.error(f"Error creating document_store table: {str(e)}")

