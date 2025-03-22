CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin INTEGER DEFAULT 0  -- 1 for admin, 0 for normal users
);

CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_option TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    score INTEGER,
    taken_at TIMESTAMP,
    time_taken INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

INSERT INTO users (username, password, is_admin)
SELECT 'admin', 'admin', 1 WHERE NOT EXISTS (SELECT 1 FROM users WHERE username='admin');
