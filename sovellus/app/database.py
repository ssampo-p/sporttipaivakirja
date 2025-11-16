
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
            CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY,
                content TEXT,
                title TEXT,
                sent_at TEXT,
                workout_level TEXT,
                sport TEXT,
                user_id INTEGER REFERENCES users
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
                comment TEXT,
                user_id INTEGER REFERENCES users,
                workout_id INTEGER REFERENCES workouts
            );
        """)
        self.connection.commit()
    
    
    def add_comment_to_workout(self, workout_id, user_id, content):
        self.cursor.execute("""
            INSERT INTO comment_threads (comment, user_id, workout_id)
            VALUES (?, ?, ?)
        """, (content, user_id, workout_id))
        self.connection.commit()
        
    def get_workout_comments(self, workout_id):
        self.cursor.execute("SELECT comment, user_id FROM comment_threads WHERE workout_id = ?", (workout_id,))       
        rows = self.cursor.fetchall()
        comments = []
        for row in rows:
            comment = row[0]
            print("rivi:", row[1])
            username = self.get_username_by_id(row[1])
            print("username:", username)
            comments.append((comment, username))
        return comments
            
            
        
    def add_workout(self,content, sent_at, user_id, title, workout_level, sport):
        self.cursor.execute("""
            INSERT INTO workouts (content, sent_at, user_id, title, workout_level, sport)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (content, sent_at, user_id, title, workout_level, sport))
        self.connection.commit()
    
    def get_workout(self,workout_id):
        self.cursor.execute("SELECT id, title, content, sent_at, workout_level, sport, user_id FROM workouts WHERE id = ?", (workout_id,))
        return self.cursor.fetchone()
    
    def get_workouts(self):
        self.cursor.execute("SELECT id, title, content, sent_at, workout_level, sport, user_id FROM workouts") 
        return self.cursor.fetchall()
    def get_workouts_by_level(self, workout_level):
        self.cursor.execute("SELECT id, title, content, sent_at, workout_level, sport, user_id FROM workouts WHERE workout_level = ?", (workout_level,))
        return self.cursor.fetchall()
    
    def delete_workout(self, workout_id):
        self.cursor.execute("DELETE FROM workouts WHERE id = ?",(workout_id,))
        self.connection.commit()
    
    def get_workouts_by_user(self, user_id):
        self.cursor.execute("SELECT id, title, content, sent_at, workout_level, sport FROM workouts WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()
    
    def edit_workout(self,new_title, new_content, workout_level, sport, workout_id, user_id,):
        self.cursor.execute("UPDATE workouts SET title = ?, content = ?, workout_level = ?, sport = ? WHERE id = ? AND user_id = ?", (new_title, new_content, workout_level, sport, workout_id, user_id)) 
        self.connection.commit()
        

    
    def add_user(self, username, password_hash):
        self.cursor.execute("""
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
        """, (username, password_hash))
        self.connection.commit()
        
    def get_user(self, username):
        self.cursor.execute("SELECT username, password_hash FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()
    
    #contains user id now
    def get_user_by_id(self, username):
        self.cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()
    def get_username_by_id(self, user_id):
        self.cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        return self.cursor.fetchone()
    
    def close(self):
        self.connection.close()

    