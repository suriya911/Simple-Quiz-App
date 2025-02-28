# questions.py
import sqlite3

def insert_default_questions():
    """
    Insert 50 default questions into the database only if the table is empty.
    """
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

    # Check if any questions exist
    cursor.execute("SELECT COUNT(*) FROM questions")
    count = cursor.fetchone()[0]

    if count == 0:
        questions = [
            ("What is 2 + 2?", "3", "4", "5", "6", "b"),
            ("What is the capital of France?", "Paris", "London", "Rome", "Berlin", "a"),
            ("Which planet is known as the Red Planet?", "Venus", "Mars", "Jupiter", "Saturn", "b"),
            ("What is the square root of 16?", "2", "3", "4", "5", "c"),
            ("Which gas do plants absorb?", "Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen", "b"),
            ("Who wrote 'Hamlet'?", "Shakespeare", "Hemingway", "Austen", "Tolstoy", "a"),
            ("What is 10 x 5?", "30", "40", "50", "60", "c"),
            ("Which country invented pizza?", "France", "Italy", "USA", "India", "b"),
            ("How many continents are there?", "5", "6", "7", "8", "c"),
            ("What is the boiling point of water?", "90°C", "100°C", "110°C", "120°C", "b"),
            # More questions ...
            ("What is the capital of Japan?", "Beijing", "Seoul", "Tokyo", "Bangkok", "c"),
            ("How many sides does a hexagon have?", "5", "6", "7", "8", "b"),
            ("Which ocean is the largest?", "Atlantic", "Indian", "Arctic", "Pacific", "d"),
            ("What is H2O commonly known as?", "Oxygen", "Hydrogen", "Water", "Helium", "c"),
            ("Which is the fastest land animal?", "Cheetah", "Lion", "Horse", "Leopard", "a"),
            ("Who painted the Mona Lisa?", "Van Gogh", "Da Vinci", "Picasso", "Michelangelo", "b"),
            ("What is 15 / 3?", "3", "4", "5", "6", "c"),
            ("Which planet is closest to the Sun?", "Earth", "Venus", "Mercury", "Mars", "c"),
            ("What is the capital of the USA?", "New York", "Los Angeles", "Washington D.C.", "Chicago", "c"),
            ("How many bones are in the human body?", "204", "206", "208", "210", "b"),
            ("What does CPU stand for?", "Central Processing Unit", "Computer Personal Unit", "Central Power Unit", "Control Processing Unit", "a"),
            ("What is the chemical symbol for Gold?", "Ag", "Au", "Pb", "Fe", "b"),
            ("Which gas do humans breathe in?", "Carbon Dioxide", "Oxygen", "Nitrogen", "Hydrogen", "b"),
            ("What is the capital of India?", "Mumbai", "Delhi", "Kolkata", "Chennai", "b"),
            ("Which programming language is best for AI?", "C++", "Java", "Python", "Swift", "c"),
            ("What is the freezing point of water?", "0°C", "10°C", "100°C", "-10°C", "a"),
            ("Who discovered gravity?", "Newton", "Einstein", "Galileo", "Tesla", "a"),
            ("Which country has the largest population?", "India", "China", "USA", "Russia", "b"),
            ("What is the capital of Australia?", "Sydney", "Melbourne", "Canberra", "Brisbane", "c"),
            ("What is the chemical symbol for Iron?", "Fe", "Ir", "In", "Io", "a"),
            ("What does HTML stand for?", "HyperText Markup Language", "High-Level Text Machine Language", "HyperTransfer Markup Language", "None of the above", "a"),
            ("What is the speed of light?", "300,000 km/s", "150,000 km/s", "500,000 km/s", "100,000 km/s", "a"),
            ("Which planet is known as the Gas Giant?", "Earth", "Mars", "Jupiter", "Venus", "c"),
            ("How many legs does a spider have?", "6", "8", "10", "12", "b"),
            ("Who was the first person to step on the Moon?", "Neil Armstrong", "Buzz Aldrin", "Yuri Gagarin", "Michael Collins", "a"),
            ("Which metal is liquid at room temperature?", "Gold", "Mercury", "Silver", "Copper", "b"),
            ("Which programming language is used for web development?", "C", "Python", "HTML", "Java", "c"),
            ("What is 50 + 25?", "70", "75", "80", "85", "b"),
            ("Who discovered America?", "Columbus", "Magellan", "Vasco da Gama", "James Cook", "a"),
            ("What is the smallest prime number?", "1", "2", "3", "5", "b"),
            ("Which country is known for the Eiffel Tower?", "USA", "France", "Germany", "Italy", "b"),
            ("How many letters are in the English alphabet?", "24", "25", "26", "27", "c"),
            ("What is 7 x 8?", "48", "54", "56", "64", "c"),
            ("Which is the national sport of Japan?", "Football", "Baseball", "Sumo Wrestling", "Cricket", "c"),
            ("Which animal is known as the King of the Jungle?", "Tiger", "Elephant", "Lion", "Gorilla", "c"),
            ("Which ocean is the coldest?", "Indian", "Pacific", "Arctic", "Atlantic", "c"),
            ("Which festival is known as the Festival of Lights?", "Eid", "Christmas", "Diwali", "Hanukkah", "c"),
            ("What is 100 divided by 10?", "5", "10", "20", "25", "b"),
            ("How many legs does a butterfly have?", "4", "6", "8", "10", "b"),
            ("What is the main ingredient in sushi?", "Fish", "Rice", "Noodles", "Tofu", "b")
        ]
        for q in questions:
            cursor.execute("""
                INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_option) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, q)
        conn.commit()
        print("✅ 50 questions inserted into the database.")
    else:
        print("✅ Questions already exist. No insertion needed.")
    conn.close()

if __name__ == "__main__":
    insert_default_questions()
