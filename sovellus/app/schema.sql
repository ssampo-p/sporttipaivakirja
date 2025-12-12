CREATE TABLE workouts (
            id INTEGER PRIMARY KEY,
                content TEXT,
                title TEXT,
                sent_at TEXT,
                workout_level TEXT,
                sport TEXT,
                user_id INTEGER REFERENCES users
           );
CREATE TABLE users (
            id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password_hash TEXT
            );
CREATE TABLE comments (
            id INTEGER PRIMARY KEY,
                comment TEXT,
                user_id INTEGER REFERENCES users,
                workout_id INTEGER REFERENCES workouts,
                sent_at TEXT
            );