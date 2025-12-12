import random
import sqlite3

#for testing purposes
db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM workouts")
db.execute("DELETE FROM comments")

user_count = 1000
workout_count = 10**5
comment_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, workout_count + 1):
    db.execute("INSERT INTO threads (title) VALUES (?)",
               ["thread" + str(i)])

for i in range(1, workout_count + 1):
    user_id = random.randint(1, user_count)
    workout_id = random.randint(1, workout_count)
    db.execute("""INSERT INTO comments (content, sent_at, user_id, workout_id)
                  VALUES (?, datetime('now'), ?, ?)""",
               ["message" + str(i), user_id, workout_id])

db.commit()
db.close()