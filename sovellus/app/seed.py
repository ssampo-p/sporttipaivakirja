import random
import sqlite3
import path # file that contais full path to the db
from datetime import datetime




#for testing purposes
db = sqlite3.connect(path.DB_PATH)

db.execute("DELETE FROM users")
db.execute("DELETE FROM workouts")
db.execute("DELETE FROM comments")


sports = [
            "Jääkiekko",
            "Jalkapallo",
            "Juoksu",
            "Kuntosali",
            "Pyöräily",
            "Tennis",
            "Padel",
            "Lentopallo",
            "Kamppailu",
            "Muu"
        ]

user_count = 1000
workout_count = 10**6
comment_count = 10**7

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, workout_count + 1):
    user_id = random.randint(1, user_count)
    sport = random.choice(sports)
    time = datetime.now().isoformat(" ")
    db.execute("""
        INSERT INTO workouts (title, content, sent_at, user_id, sport)
        VALUES (?, ?, ?, ?, ?)""",
        (f"workout_title_{i}",f"workout_content_{i}",
        time,
        user_id,
        sport
    ))
    
    
for i in range(1, comment_count + 1):
    user_id = random.randint(1, user_count)
    workout_id = random.randint(1, workout_count)
    time = datetime.now().isoformat(" ")
    db.execute("""
        INSERT INTO comments (comment, user_id, workout_id, sent_at)
        VALUES (?, ?, ?, ?)""",
        (f"comment_{i}",user_id,workout_id, time))

#index
db.execute("CREATE INDEX idx_workouts ON workouts (sent_at DESC)")             # if only the basic workout page is loaded
db.execute("CREATE INDEX idx_workouts_sort ON workouts (sport, sent_at DESC)") # if sorting is done by sport
db.execute("CREATE INDEX idx_comments ON comments (workout_id, sent_at DESC)") # speed up the search for comments on a specific workout

db.commit()
db.close()