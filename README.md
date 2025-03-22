# Simple Quiz App (Flask + SQLite)

Welcome to the **Simple Quiz App**, a dynamic and user-friendly web-based quiz application built using **Flask** and **SQLite**. Test your knowledge, compete with friends, and challenge yourself with a variety of questions!

## 🌐 Live Demo

Try the live version here: **[Simple Quiz App](https://simple-quiz-app-8fdd.onrender.com)**

## 🚀 Features

- **User Registration & Login** 👤
- **Engaging Quiz Experience** 🎯 (20 randomized questions per session)
- **Admin Panel** 🛠 (Add & Manage Questions, View Results)
- **Session Persistence** 🔄 (Users remain logged in across sessions)
- **Preloaded Questions** 📚 (50 default questions inserted if the database is empty)
- **Responsive UI** 🖥️ (Works on mobile & desktop)
- **Real-Time Score Display** 📊

## 🛠 Installation & Setup

Follow these steps to run the app locally:

### 1️⃣ Clone the repository:

```bash
git clone https://github.com/yourusername/Simple-Quiz-App.git
cd Simple-Quiz-App
```

### 2️⃣ Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3️⃣ Install dependencies:

```bash
pip install -r requirements.txt
```

### 4️⃣ Initialize the database:

```bash
python -c "from app import init_db; init_db()"
```

### 5️⃣ Run the application:

```bash
python app.py
```

### 6️⃣ Open your browser and visit:

- **User Login:** [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login)
- **Admin Login:** [http://127.0.0.1:5000/admin_login](http://127.0.0.1:5000/admin_login)
  - Default Credentials: **Username:** `admin`, **Password:** `admin`

## 📂 Project Structure

```
SIMPLE-QUIZ-APP/
|
├── __pycache__/                       # Python cache files
|
├── .github/workflows/                # GitHub Actions workflows
|   └── deploy.yml                    # Deployment configuration
|
├── instance/                         # Instance folder for database
|   └── session.db                    # Session database
|
├── static/                           # Static files (CSS, JS)
|   ├── css/
|   |   └── styles.css                # Stylesheet
|   |
|   └── js/
|       └── scripts.js                # JavaScript file
|
├── templates/                        # HTML templates
|   ├── admin_login.html              # Admin login page
|   ├── admin.html                    # Admin dashboard
|   ├── base.html                     # Base template
|   ├── home.html                     # Home page
|   ├── login.html                    # User login page
|   ├── logo.html                     # Logo template/component
|   ├── manage_questions.html        # Admin question management
|   ├── quiz.html                     # Quiz page
|   ├── register.html                 # User registration page
|   ├── user.html                     # User dashboard
|   └── view_results.html            # Results viewing page
|
├── app.py                            # Main Flask application
├── Procfile                          # Process file for deployment
├── questions.py                      # Script to insert questions
├── quiz.db                           # Quiz database
├── README.md                         # Project documentation
├── requirements.txt                  # Python dependencies
└── schema.sql

```

## ⚙️ CI/CD Pipeline (GitHub Actions & Render)

This project includes an automated deployment pipeline using **GitHub Actions** and **Render**:

- **Continuous Deployment:** Any code pushed to the `main` branch is automatically deployed to Render.
- **Database Initialization:** The database is updated during every deployment to reflect new users, new questions, and admin changes.
- **Automatic Build & Deployment:** Ensures that changes are live instantly!

## 👨‍💻 Tech Stack

- **Python** (Flask Framework)
- **SQLite** (Lightweight Database)
- **Bootstrap** (Modern UI Styling)
- **GitHub Actions + Render** (CI/CD & Hosting)

## 📜 License

This project is **open-source** and free to use. Feel free to modify and improve it!

## 🎯 Future Enhancements

- Implement a quiz **timer** ⏳
- Add **user analytics & leaderboards** 📊
- Improve **UI animations & themes** ✨
- Expand to **multiple-choice and fill-in-the-blank** questions

---

💡 **Contribute & Star ⭐ this project if you like it!**

Happy coding! 🚀
