# app.py
from flask import Flask, render_template, request, redirect, url_for, session, g, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key
DATABASE = 'quiz.db'


# Database connection helper
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # This allows us to use column names
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Initialize the database using the schema.sql file
def init_db():
    with app.app_context():
        db = get_db()
        with open('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        print("Initialized the database.")


# ---------------------------
# Routes
# ---------------------------

# Home Page (redirects to quiz if logged in)
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('quiz'))
    return redirect(url_for('login'))


# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
         username = request.form['username']
         password = request.form['password']
         db = get_db()
         try:
             db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
             db.commit()
             flash("Registration successful, please login.", "success")
             return redirect(url_for('login'))
         except sqlite3.IntegrityError:
             flash("Username already exists", "danger")
    return render_template('register.html')


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
         username = request.form['username']
         password = request.form['password']
         db = get_db()
         cur = db.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
         user = cur.fetchone()
         if user:
             session['user_id'] = user['id']
             session['username'] = user['username']
             session['is_admin'] = user['is_admin']
             flash("Logged in successfully", "success")
             return redirect(url_for('quiz'))
         else:
             flash("Invalid credentials", "danger")
    return render_template('login.html')


# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for('login'))


# Quiz Route
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'user_id' not in session:
         flash("Please login first", "warning")
         return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
         # Process the submitted quiz answers
         score = 0
         # For each of the 20 questions, check the answer
         for key in request.form:
             if key.startswith('answer_'):
                 q_id = key.split('_')[1]
                 user_answer = request.form.get(key)
                 cur = db.execute("SELECT correct_option FROM questions WHERE id = ?", (q_id,))
                 question = cur.fetchone()
                 if question and user_answer == question['correct_option']:
                      score += 1
         # Save the result
         db.execute("INSERT INTO results (user_id, score) VALUES (?, ?)", (session['user_id'], score))
         db.commit()
         flash(f"You scored {score} out of 20", "info")
         return redirect(url_for('result'))
    else:
         # GET request: load 20 random questions
         cur = db.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 20")
         questions = cur.fetchall()
         return render_template('quiz.html', questions=questions)


# Route to view a user's quiz results
@app.route('/result')
def result():
    if 'user_id' not in session:
         flash("Please login first", "warning")
         return redirect(url_for('login'))
    db = get_db()
    cur = db.execute("SELECT * FROM results WHERE user_id = ? ORDER BY taken_at DESC", (session['user_id'],))
    results = cur.fetchall()
    return render_template('result.html', results=results)


# ---------------------------
# Admin Routes
# ---------------------------

# Admin Dashboard: view all questions and user results
@app.route('/admin')
def admin():
    if not session.get('is_admin'):
         flash("Admin access required", "danger")
         return redirect(url_for('login'))
    db = get_db()
    cur = db.execute("SELECT * FROM questions")
    questions = cur.fetchall()
    cur = db.execute("""
        SELECT r.*, u.username 
        FROM results r 
        JOIN users u ON r.user_id = u.id 
        ORDER BY r.taken_at DESC
    """)
    results = cur.fetchall()
    return render_template('admin.html', questions=questions, results=results)


# Route for admin to add a new question
@app.route('/admin/add_question', methods=['GET', 'POST'])
def add_question():
    if not session.get('is_admin'):
         flash("Admin access required", "danger")
         return redirect(url_for('login'))
    if request.method == 'POST':
         question_text = request.form['question']
         option_a = request.form['option_a']
         option_b = request.form['option_b']
         option_c = request.form['option_c']
         option_d = request.form['option_d']
         correct_option = request.form['correct_option']
         db = get_db()
         db.execute("""
            INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_option)
            VALUES (?, ?, ?, ?, ?, ?)
         """, (question_text, option_a, option_b, option_c, option_d, correct_option))
         db.commit()
         flash("Question added successfully", "success")
         return redirect(url_for('admin'))
    return render_template('add_question.html')


# Route for admin to delete a question
@app.route('/admin/delete_question/<int:question_id>')
def delete_question(question_id):
    if not session.get('is_admin'):
         flash("Admin access required", "danger")
         return redirect(url_for('login'))
    db = get_db()
    db.execute("DELETE FROM questions WHERE id = ?", (question_id,))
    db.commit()
    flash("Question deleted successfully", "success")
    return redirect(url_for('admin'))


# ---------------------------
# Main
# ---------------------------
if __name__ == '__main__':
    # Initialize the database if it doesn't exist
    if not os.path.exists(DATABASE):
         init_db()
    app.run(debug=True)
