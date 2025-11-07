
import sqlite3


'''
        Class for handling database operations
'''
class Database:
    
    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
        self.create_tables()
        
    def create_tables(self):
        
        ''' Creates necessary tables if they don't exist '''
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
                content TEXT,
                sent_at TEXT,
                user_id INTEGER REFERENCES users,
                thread_id INTEGER REFERENCES threads
           );
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password_hash TEXT
            );
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS comment_threads (
            id INTEGER PRIMARY KEY,
                title TEXT,
                user_id INTEGER REFERENCES users,
                message_id INTEGER REFERENCES messages
            );
        """)
        self.connection.commit()
        
    def add_message(self,content, sent_at, user_id, thread_id):
        self.cursor.execute("""
            INSERT INTO messages (content, sent_at, user_id, thread_id)
            VALUES (?, ?, ?, ?)
        """, (content, sent_at, user_id, thread_id))
        self.connection.commit()
        
    def get_messages(self):
        self.cursor.execute("SELECT * FROM messages") # TODO: add WHERE clause for threads ?
        return self.cursor.fetchall()
    
    def add_user(self, username, password_hash):
        self.cursor.execute("""
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
        """, (username, password_hash))
        self.connection.commit()
        
    def get_user(self, username):
        self.cursor.execute("SELECT username, password_hash FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()
        
    
    def close(self):
        self.connection.close()

    