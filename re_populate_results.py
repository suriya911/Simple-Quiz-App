import sqlite3
import random

# Connect to your database
conn = sqlite3.connect('quiz.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Step 1: Fetch all rows from the results table.
cursor.execute("SELECT user_id, score, taken_at, time_taken FROM results")
rows = cursor.fetchall()

# Step 2: Deduplicate rows.
# We'll consider two rows duplicates if they share the same user_id and taken_at.
unique_rows = {}
for row in rows:
    key = (row['user_id'], row['taken_at'])
    if key not in unique_rows:
        unique_rows[key] = row
deduped_rows = list(unique_rows.values())

# Step 3: Clear the results table.
cursor.execute("DELETE FROM results")
conn.commit()

# Reset the auto-increment counter by deleting the corresponding row from sqlite_sequence.
cursor.execute("DELETE FROM sqlite_sequence WHERE name='results'")
conn.commit()

# Step 4: Re-insert rows with randomized score and time_taken.
# We preserve user_id and taken_at (date and time remain unchanged).
# Randomize score (0-20) and time_taken (0-300) for each row.
for row in deduped_rows:
    new_score = random.randint(0, 20)
    new_time_taken = random.randint(0, 300)
    cursor.execute(
        "INSERT INTO results (user_id, score, taken_at, time_taken) VALUES (?, ?, ?, ?)",
        (row['user_id'], new_score, row['taken_at'], new_time_taken)
    )
conn.commit()

conn.close()
print("Results table re-populated with new random score and time_taken values, and the id renumbered from 1.")
