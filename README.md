# Simple Quiz App (Flask + SQLite)

Welcome to the **Simple Quiz App**, a lightweight and easy-to-use web-based quiz application built with **Flask** and **SQLite**. This app allows users to register, log in, take quizzes, and view their scores. Admins can manage quiz questions and view results.

## 🚀 Features

- **User Registration & Login**
- **Randomized Quiz** (20 questions per session)
- **Admin Panel** (Manage Questions & View Results)
- **Persistent Session Storage** (Sessions remain even after restarting)
- **Automatic Question Insertion** (50 default questions added if none exist)
- **Results Displayed in a Table Format**

## 🛠 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/Simple-Quiz-App.git
   cd Simple-Quiz-App
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python app.py
   ```

5. Open your browser and go to:
   - **User Login:** [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login)
   - **Admin Login:** [http://127.0.0.1:5000/admin_login](http://127.0.0.1:5000/admin_login)  
     (Use credentials: **Username:** `admin`, **Password:** `admin`)

## 📂 Project Structure

```
Simple-Quiz-App/
│
├── app.py                 # Main Flask application
├── schema.sql             # Database schema
├── insert_questions.py    # Auto-adds questions if empty
├── quiz.db                # SQLite database
├── requirements.txt       # Required Python packages
└── templates/             # HTML templates
    ├── base.html
    ├── login.html
    ├── register.html
    ├── quiz.html
    ├── result.html
    ├── admin.html
    ├── view_results.html
    ├── manage_questions.html
```

## 👨‍💻 Tech Stack

- **Python** (Flask)
- **SQLite** (Database)
- **Bootstrap** (Frontend UI)

## 📜 License

This project is **open-source** and free to use. Feel free to modify and improve it!

## 🎯 Future Enhancements

- Add a timer for quizzes ⏳
- Implement user analytics 📊
- Improve UI with animations ✨

Happy coding! 🚀
