import sqlite3

# Connect to database
conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

# Sample questions
sample_questions = [
    ("What is the capital of France?", "Paris", "London", "Rome", "Berlin", "a"),
    ("Which programming language is known for AI?", "C++", "Java", "Python", "Ruby", "c"),
    ("What is 2 + 2?", "3", "4", "5", "6", "b"),
    ("Which planet is known as the Red Planet?", "Venus", "Mars", "Jupiter", "Saturn", "b"),
    ("What is the largest ocean on Earth?", "Atlantic", "Indian", "Arctic", "Pacific", "d")
]

# Insert data
for q in sample_questions:
    cursor.execute("INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_option) VALUES (?, ?, ?, ?, ?, ?)", q)

# Commit and close
conn.commit()
conn.close()
print("Sample questions inserted into the database.")
