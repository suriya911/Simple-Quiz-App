# 🤔 Simple Quiz App (Flask + SQLite + Docker + AWS)

Welcome to **Simple Quiz App**, a dynamic, secure, and responsive web-based quiz platform built with **Flask** and **SQLite**, designed for learning, testing knowledge, and managing quizzes with ease. Experience seamless user and admin interactions with real-time score tracking and robust analytics!

---

## 🌐 Live Demo

👉 Try it here: **[Simple Quiz App (Render)](https://simple-quiz-app-8fdd.onrender.com)**  
👉 Try it here: **[Simple Quiz App (AWS)](http://simple-quiz-env.eba-pjwgugz9.us-east-1.elasticbeanstalk.com/home)**  
_(Hosted via Render & AWS Elastic Beanstalk – auto-deployed from GitHub Actions)_

---

## 🚀 Features

- 👤 **User Registration & Login**
- 🎯 **Timed Quiz Experience** (20 Random Questions per Session)
- 🛡️ **Secure Session Management**
- 🧑‍💼 **Admin Panel** (Add/Delete Questions, View Results)
- 📊 **Score Tracking + Top Performer Leaderboard**
- 📈 **Histogram + Normal Curve Visualization**
- 📂 **Session Persistence** (SQLite + Flask-Session)
- 🌙 **Responsive UI (Mobile + Desktop)**
- 🩩 **Real-time Quiz Timer & Auto Submission**

---

## 🛠️ Software Stack

| Layer            | Technology               |
| ---------------- | ------------------------ |
| Frontend         | HTML5, Bootstrap, JS     |
| Backend          | Python (Flask Framework) |
| Database         | SQLite3                  |
| CI/CD            | GitHub Actions + Render  |
| Containerization | Docker                   |
| Cloud Deploy     | AWS (ECR, ECS)           |
| Hosting (Web)    | Render, Docker, AWS      |

---

## 📊 Architecture Diagram (AWS Deployment)

```plaintext
+-------------------+
|  User's Browser   |
+--------+----------+
         |
         v
+----------------------------+
| AWS Elastic Load Balancer |
+--------+-------------------+
         |
         v
+----------------------------+
| Elastic Beanstalk Service |
| (Docker Container Host)   |
+--------+-------------------+
         |
         v
+----------------------------+
|  EC2 Instance (Flask App)  |
|  Running Gunicorn Server   |
+--------+-------------------+
         |
         v
+----------------------------+
|  SQLite DB (Local Storage) |
+----------------------------+
```

---

## 🔒 Security Implementation

- 🔑 **Session Management:** Flask-Session with server-side session storage (SQLAlchemy).
- 🚫 **Admin Protection:** Restricted `/admin` access, enforced role checks.
- 🦫 **UUID Tokenization:** Prevent duplicate quiz submissions.
- 🕵️ **Password Storage:** _[To be enhanced with hashing]_.
- 🥷️ **CSRF Prevention:** Form validation and token validation.
- 🔐 **CI/CD Secrets:** Docker Hub, Render, AWS credentials secured via GitHub Secrets.

---

## 🥚 Test Cases – API Testing

### Manual Testing:

| Feature          | Method   | Endpoint            | Expected Outcome                     |
| ---------------- | -------- | ------------------- | ------------------------------------ |
| User Register    | POST     | `/register`         | Registers new user                   |
| User Login       | POST     | `/login`            | Authenticates and redirects          |
| Quiz Start       | GET      | `/quiz`             | Displays 20 randomized questions     |
| Quiz Submit      | POST     | `/quiz`             | Submits answers and calculates score |
| View Results     | GET      | `/view_results`     | Shows user's past attempts           |
| Admin Login      | POST     | `/admin_login`      | Verifies admin and shows dashboard   |
| Manage Questions | POST/GET | `/manage_questions` | Add/Delete quiz questions            |

---

## ⚙️ CI/CD Integration

### GitHub Actions – `deploy.yml` Highlights

- 🔄 **Auto Build + Deploy** on push to `main`
- 🐿 **Docker Image Build + Push** to Docker Hub
- 🌍 **Trigger Deploy** via Render API
- ☁️ **Push to AWS ECR** + Deploy to ECS
- 📸 **CI Screenshot:**

![CI Screenshot](https://i.imgur.com/ci-placeholder.png) _(Upload real screenshot of GitHub Actions run)_

---

## 📦 Installation & Local Setup

### 1️⃣ Clone Repo:

```bash
git clone https://github.com/yourusername/Simple-Quiz-App.git
cd Simple-Quiz-App
```

### 2️⃣ Create Virtual Env:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies:

```bash
pip install -r requirements.txt
```

### 4️⃣ Initialize Database:

```bash
python -c "from app import init_db; init_db()"
```

### 5️⃣ Run App:

```bash
python app.py
```

### 6️⃣ Access Locally:

- User Login: `http://127.0.0.1:5000/login`
- Admin Login: `http://127.0.0.1:5000/admin_login`  
  Default: **Username:** `admin` | **Password:** `admin`

---

## 🐳 Docker Deployment (Local)

### Build Docker Image:

```bash
docker build -t myusername/myapp:latest .
```

### Run Container:

```bash
docker run -d -p 5000:5000 myusername/myapp:latest
```

Access: `http://localhost:5000`

---

## 🛫 Deployment (Render + AWS)

- **Render:** Auto-deploys from GitHub via API.
- **AWS:** Docker image pushed to **ECR**, deployed via **Elastic Beanstalk (Docker Host)**.
- See **`.github/workflows/deploy.yml`** for CI/CD config.

---

## 📂 Project Structure

```
SIMPLE-QUIZ-APP/
﻿|
├── app.py                 # Main Flask App
├── questions.py           # Preload default quiz questions
├── schema.sql             # DB Schema
├── requirements.txt       # Python Dependencies
├── Dockerfile             # Docker Build File
├── Procfile               # For Heroku/Render (if needed)
├── templates/             # HTML Templates
├── static/                # CSS + JS
├── quiz.db                # SQLite Database
├── .github/workflows/     # GitHub Actions (CI/CD)
│   └── deploy.yml
└── README.md              # This File!
```

---

## 🌟 Future Enhancements

- 🔒 Password Hashing + Email Verification
- 🧠 AI-based Question Recommendation
- 🏆 Leaderboards + Badges
- 📊 Admin Analytics Dashboard
- 🌈 Theme Customization (Light/Dark)

---

## 📜 License

This project is open-source under the MIT License.  
**Feel free to contribute, fork, and star ⭐ this repo!**

---

## 💻 Developer Note

Crafted with ❤️ for Cloud Computing enthusiasts.  
For queries or contributions, open an issue or pull request!

---
