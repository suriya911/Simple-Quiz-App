from flask import Flask, render_template, request, redirect, url_for, session, g, flash, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from questions import insert_default_questions
import sqlite3
import os
import datetime
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = 'quiz.db'

app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///session.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db

Session(app)

@app.template_filter('format_date')
def format_date(value, format='%d-%m-%Y %I:%M:%S %p'):
    try:
        dt = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return dt.strftime(format)
    except Exception as e:
        print("Date formatting error:", e)
        return value

def get_db():
    database = getattr(g, '_database', None)
    if database is None:
        database = g._database = sqlite3.connect(DATABASE)
        database.row_factory = sqlite3.Row
    return database

@app.teardown_appcontext
def close_connection(exception):
    database = getattr(g, '_database', None)
    if database is not None:
        database.close()

def init_db():
    with app.app_context():
        database = get_db()
        with open('schema.sql', mode='r') as f:
            database.cursor().executescript(f.read())
        database.commit()
        print("Initialized the database.")

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
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
            if user['is_admin']:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/user')
def user_dashboard():
    if 'user_id' not in session:
        flash("Please log in first", "warning")
        return redirect(url_for('login'))
    if session.get('is_admin'):
        return redirect(url_for('admin'))
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        greeting = "Good Morning"
    elif current_hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
    return render_template("user.html", greeting=greeting)

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for('home'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'user_id' not in session:
        session['user_id'] = 1

    db_conn = get_db()
    action = request.args.get('action', 'new')
    if action == 'new':
        session.pop('quiz_start_time', None)
        session.pop('quiz_questions', None)
        session.pop('quiz_remaining_time', None)
        session.pop('quiz_score', None)
        session.pop('quiz_elapsed', None)

    if request.method == 'GET':
        if action == 'new' or 'quiz_questions' not in session:
            cur = db_conn.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 20")
            questions = cur.fetchall()
            session['quiz_questions'] = [dict(q) for q in questions]
            session['quiz_remaining_time'] = 300
            session['quiz_start_time'] = time.time()
        else:
            questions = session.get('quiz_questions')
        return render_template('quiz.html',
                               questions=questions,
                               remaining_time=session.get('quiz_remaining_time', 300))
    else:
        score = 0
        for key, value in request.form.items():
            if key.startswith('answer_'):
                q_id = key.split('_')[1]
                user_answer = value
                cur = db_conn.execute("SELECT correct_option FROM questions WHERE id = ?", (q_id,))
                question = cur.fetchone()
                if question and user_answer == question['correct_option']:
                    score += 1

        total_duration = 300
        remaining_str = request.form.get('remaining_time')
        try:
            remaining = int(remaining_str) if remaining_str is not None else session.get('quiz_remaining_time', total_duration)
        except ValueError:
            remaining = total_duration

        quiz_taken_time = total_duration - remaining

        session['quiz_score'] = score
        session['quiz_elapsed'] = quiz_taken_time

        local_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            db_conn.execute(
                "INSERT INTO results (user_id, score, time_taken, taken_at) VALUES (?, ?, ?, ?)",
                (session['user_id'], score, quiz_taken_time, local_time)
            )
            db_conn.commit()
        except Exception as e:
            print("Error inserting quiz result:", e)
            return jsonify({'error': 'Failed to store quiz result.'}), 500

        cur = db_conn.execute(
            "SELECT COUNT(*) as cnt FROM results WHERE user_id = ? AND taken_at = ? AND score = ? AND time_taken = ?",
            (session['user_id'], local_time, score, quiz_taken_time)
        )
        cnt = cur.fetchone()['cnt']
        if cnt > 1:
            db_conn.execute(
                "DELETE FROM results WHERE id = (SELECT id FROM results WHERE user_id = ? AND taken_at = ? AND score = ? AND time_taken = ? ORDER BY id DESC LIMIT 1)",
                (session['user_id'], local_time, score, quiz_taken_time)
            )
            db_conn.commit()

        session.pop('quiz_start_time', None)
        session.pop('quiz_questions', None)
        session.pop('quiz_remaining_time', None)

        return jsonify({'score': score, 'elapsed_seconds': quiz_taken_time})

@app.route('/update_quiz_state', methods=['POST'])
def update_quiz_state():
    question_id = request.form.get('question_id')
    answer = request.form.get('answer')
    if 'quiz_answers' not in session:
        session['quiz_answers'] = {}
    session['quiz_answers'][question_id] = answer
    session.modified = True
    return '', 204

@app.route('/update_quiz_timer', methods=['POST'])
def update_quiz_timer():
    remaining = request.form.get('remaining_time') or request.args.get('remaining_time')
    try:
        remaining = int(remaining)
    except (TypeError, ValueError):
        remaining = 300
    session['quiz_remaining_time'] = remaining
    return '', 204

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
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
    db_conn = get_db()

    def rows_to_dicts(rows):
        return [dict(row) for row in rows]

    if session.get('is_admin'):
        query_all = """
            SELECT r.score, r.taken_at, r.time_taken, u.username 
            FROM results r 
            JOIN users u ON r.user_id = u.id 
            ORDER BY r.taken_at DESC
        """
        all_results = rows_to_dicts(db_conn.execute(query_all).fetchall())

        admin_best_query = """
            SELECT username, score, time_taken, taken_at FROM (
              SELECT u.username, r.score, r.time_taken, r.taken_at,
                     ROW_NUMBER() OVER (PARTITION BY u.id ORDER BY r.score DESC, r.time_taken ASC) as rn
              FROM results r 
              JOIN users u ON r.user_id = u.id
            ) sub
            WHERE rn = 1
            ORDER BY score DESC, time_taken ASC
        """
        top_results = rows_to_dicts(db_conn.execute(admin_best_query).fetchall())

        graph_query = """
            SELECT r.score, u.username, r.taken_at 
            FROM results r 
            JOIN users u ON r.user_id = u.id 
            ORDER BY r.taken_at ASC
        """
        graph_data = rows_to_dicts(db_conn.execute(graph_query).fetchall())
    else:
        user_id = session.get('user_id')
        query_all = """
            SELECT r.score, r.taken_at, r.time_taken, u.username 
            FROM results r 
            JOIN users u ON r.user_id = u.id 
            WHERE u.id = ? 
            ORDER BY r.taken_at DESC
        """
        all_results = rows_to_dicts(db_conn.execute(query_all, (user_id,)).fetchall())

        user_top_query = """
            SELECT u.username, r.score, r.time_taken, r.taken_at
            FROM results r 
            JOIN users u ON r.user_id = u.id
            WHERE u.id = ?
            ORDER BY r.score DESC, r.time_taken ASC
            LIMIT 3
        """
        top_results = rows_to_dicts(db_conn.execute(user_top_query, (user_id,)).fetchall())

        graph_query = """
            SELECT r.score, u.username, r.taken_at 
            FROM results r 
            JOIN users u ON r.user_id = u.id 
            WHERE u.id = ? 
            ORDER BY r.taken_at ASC
        """
        graph_data = rows_to_dicts(db_conn.execute(graph_query, (user_id,)).fetchall())

    return render_template("view_results.html",
                           all_results=all_results,
                           top_results=top_results,
                           graph_data=graph_data)


if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
        insert_default_questions()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
