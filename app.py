# app.py
from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from questions import insert_default_questions
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key in production
DATABASE = 'quiz.db'

# Configure Flask-Session to use SQLAlchemy for persistent sessions
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///session.db'  # Separate session storage
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy for session management
db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db

# Initialize Session
Session(app)


# ---------------------------
# Database Helpers
# ---------------------------
def get_db():
    """
    Helper function to get a SQLite database connection.
    Uses Flask's g object to store the connection per request.
    """
    database = getattr(g, '_database', None)
    if database is None:
        database = g._database = sqlite3.connect(DATABASE)
        database.row_factory = sqlite3.Row  # Allow accessing columns by name
    return database

@app.teardown_appcontext
def close_connection(exception):
    """
    Closes the database connection at the end of the request.
    """
    database = getattr(g, '_database', None)
    if database is not None:
        database.close()

def init_db():
    """
    Initializes the database using the schema.sql file.
    """
    with app.app_context():
        database = get_db()
        with open('schema.sql', mode='r') as f:
            database.cursor().executescript(f.read())
        database.commit()
        print("Initialized the database.")


# ---------------------------
# Routes for All Users
# ---------------------------
@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    User registration. Prevents registering as 'admin'.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username.lower() == "admin":
            flash("Cannot register as admin!", "danger")
            return redirect(url_for('register'))

        db_conn = get_db()
        try:
            db_conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db_conn.commit()
            flash("Registration successful, please login.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists", "danger")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login route.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db_conn = get_db()
        cur = db_conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
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

@app.route('/logout')
def logout():
    """
    Logs out the user and clears the session.
    """
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for('login'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    """
    Displays a quiz of 20 random questions and processes the submitted answers.
    """
    if 'user_id' not in session:
        flash("Please login first", "warning")
        return redirect(url_for('login'))
    db_conn = get_db()
    if request.method == 'POST':
        score = 0
        # Evaluate each answer submitted
        for key in request.form:
            if key.startswith('answer_'):
                q_id = key.split('_')[1]
                user_answer = request.form.get(key)
                cur = db_conn.execute("SELECT correct_option FROM questions WHERE id = ?", (q_id,))
                question = cur.fetchone()
                if question and user_answer == question['correct_option']:
                    score += 1
        # Save the result
        db_conn.execute("INSERT INTO results (user_id, score) VALUES (?, ?)", (session['user_id'], score))
        db_conn.commit()
        flash(f"You scored {score} out of 20", "info")
        return redirect(url_for('result'))
    else:
        cur = db_conn.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 20")
        questions = cur.fetchall()
        return render_template('quiz.html', questions=questions)

@app.route('/result')
def result():
    """
    Displays the logged-in user's quiz results.
    """
    if 'user_id' not in session:
        flash("Please login first", "warning")
        return redirect(url_for('login'))
    db_conn = get_db()
    cur = db_conn.execute("SELECT * FROM results WHERE user_id = ? ORDER BY taken_at DESC", (session['user_id'],))
    results = cur.fetchall()
    return render_template('result.html', results=results)


# ---------------------------
# Admin Routes
# ---------------------------
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    """
    Admin login route.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db_conn = get_db()
        cur = db_conn.execute("SELECT * FROM users WHERE username = ? AND password = ? AND is_admin = 1", (username, password))
        admin = cur.fetchone()
        if admin:
            session['user_id'] = admin['id']
            session['username'] = admin['username']
            session['is_admin'] = 1
            flash("Admin login successful", "success")
            return redirect(url_for('admin'))
        else:
            flash("Invalid admin credentials", "danger")
    return render_template('admin_login.html')

@app.route('/admin')
def admin():
    """
    Admin dashboard showing all questions and quiz results.
    """
    if not session.get('is_admin'):
        flash("Admin access required", "danger")
        return redirect(url_for('login'))
    db_conn = get_db()
    cur = db_conn.execute("SELECT * FROM questions")
    questions = cur.fetchall()
    cur = db_conn.execute("""
        SELECT r.*, u.username 
        FROM results r 
        JOIN users u ON r.user_id = u.id 
        ORDER BY r.taken_at DESC
    """)
    results = cur.fetchall()
    return render_template('admin.html', questions=questions, results=results)

@app.route('/manage_questions', methods=['GET', 'POST'])
def manage_questions():
    """
    Admin route to add a new question and view all existing questions.
    """
    if not session.get('is_admin'):
        flash("Admin access required", "danger")
        return redirect(url_for('login'))
    db_conn = get_db()
    if request.method == 'POST':
        question_text = request.form['question']
        option_a = request.form['option_a']
        option_b = request.form['option_b']
        option_c = request.form['option_c']
        option_d = request.form['option_d']
        correct_option = request.form['correct_option']
        db_conn.execute("""
            INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_option)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (question_text, option_a, option_b, option_c, option_d, correct_option))
        db_conn.commit()
        flash("Question added successfully", "success")
        return redirect(url_for('manage_questions'))
    else:
        cur = db_conn.execute("SELECT * FROM questions")
        questions = cur.fetchall()
        return render_template('manage_questions.html', questions=questions)

@app.route('/admin/delete_question/<int:question_id>')
def delete_question(question_id):
    """
    Admin route to delete a question.
    """
    if not session.get('is_admin'):
        flash("Admin access required", "danger")
        return redirect(url_for('login'))
    db_conn = get_db()
    db_conn.execute("DELETE FROM questions WHERE id = ?", (question_id,))
    db_conn.commit()
    flash("Question deleted successfully", "success")
    return redirect(url_for('manage_questions'))

@app.route('/view_results')
def view_results():
    """
    Admin route to view all quiz results.
    """
    if not session.get('is_admin'):
        flash("Admin access required", "danger")
        return redirect(url_for('login'))
    db_conn = get_db()
    cur = db_conn.execute("""
        SELECT u.username, r.score, r.taken_at
        FROM results r 
        JOIN users u ON r.user_id = u.id 
        ORDER BY r.taken_at DESC
    """)
    results = cur.fetchall()
    return render_template('view_results.html', results=results)


# ---------------------------
# Main Entry Point
# ---------------------------
if __name__ == '__main__':
    # Initialize the database if it doesn't exist
    if not os.path.exists(DATABASE):
        init_db()
    # Insert default questions if none exist
    insert_default_questions()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
