import json
import os
import random
import time
from datetime import datetime

DATA_FILE = "quiz_data.json"


# ----------------- DATA MANAGEMENT -----------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"questions": [], "history": []}

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ----------------- QUESTION MANAGEMENT -----------------

def add_question(data):
    question = input("Enter question: ")
    options = []

    for i in range(4):
        opt = input(f"Option {i+1}: ")
        options.append(opt)

    correct = int(input("Correct option number (1-4): ")) - 1

    data["questions"].append({
        "question": question,
        "options": options,
        "correct": correct
    })

    save_data(data)
    print("Question added successfully.")


def show_questions(data):
    if not data["questions"]:
        print("No questions available.")
        return

    for i, q in enumerate(data["questions"], 1):
        print(f"{i}. {q['question']}")


# ----------------- QUIZ ENGINE -----------------

def start_quiz(data):
    if not data["questions"]:
        print("No questions available.")
        return

    num = int(input("How many questions? "))
    selected = random.sample(data["questions"], min(num, len(data["questions"])))

    score = 0
    start_time = time.time()

    for i, q in enumerate(selected, 1):
        print(f"\nQuestion {i}: {q['question']}")
        for idx, opt in enumerate(q["options"], 1):
            print(f"{idx}. {opt}")

        answer = int(input("Your answer: ")) - 1

        if answer == q["correct"]:
            print("Correct!")
            score += 1
        else:
            print("Wrong!")

    end_time = time.time()
    duration = round(end_time - start_time, 2)

    print("\nQuiz Finished!")
    print(f"Score: {score}/{len(selected)}")
    print(f"Time taken: {duration} seconds")

    data["history"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "score": score,
        "total": len(selected),
        "time": duration
    })

    save_data(data)


# ----------------- STATISTICS -----------------

def show_statistics(data):
    if not data["history"]:
        print("No quiz history available.")
        return

    total_attempts = len(data["history"])
    avg_score = sum(h["score"] for h in data["history"]) / total_attempts

    best = max(data["history"], key=lambda x: x["score"])
    worst = min(data["history"], key=lambda x: x["score"])

    print(f"\nTotal Attempts: {total_attempts}")
    print(f"Average Score: {avg_score:.2f}")
    print(f"Best Score: {best['score']}/{best['total']}")
    print(f"Worst Score: {worst['score']}/{worst['total']}")


# ----------------- MENU -----------------

def menu():
    print("\n=== QUIZ & EXAM ENGINE ===")
    print("1. Add Question")
    print("2. Show Questions")
    print("3. Start Quiz")
    print("4. View Statistics")
    print("5. Exit")


def main():
    data = load_data()

    while True:
        menu()
        choice = input("Choose an option: ")

        if choice == "1":
            add_question(data)
        elif choice == "2":
            show_questions(data)
        elif choice == "3":
            start_quiz(data)
        elif choice == "4":
            show_statistics(data)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
