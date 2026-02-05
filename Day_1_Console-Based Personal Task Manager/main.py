import json
import os
from datetime import datetime

USERS_FILE = "users.json"
TASKS_FILE = "tasks.json"


# ------------------ FILE HANDLING ------------------

def load_data(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)


def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


# ------------------ USER SYSTEM ------------------

def register_user(users):
    username = input("Create username: ").strip()
    if username in users:
        print("❌ Username already exists.")
        return None

    password = input("Create password: ").strip()
    users[username] = {"password": password}
    save_data(USERS_FILE, users)
    print("✅ Registration successful!")
    return username


def login_user(users):
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if username in users and users[username]["password"] == password:
        print(f"✅ Welcome back, {username}!")
        return username
    else:
        print("❌ Invalid login.")
        return None


# ------------------ TASK MANAGEMENT ------------------

def add_task(tasks, user):
    title = input("Task title: ")
    priority = input("Priority (Low / Medium / High): ")
    deadline = input("Deadline (YYYY-MM-DD): ")

    try:
        datetime.strptime(deadline, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format.")
        return

    task = {
        "title": title,
        "priority": priority,
        "deadline": deadline,
        "completed": False,
        "created_at": str(datetime.now())
    }

    tasks[user].append(task)
    save_data(TASKS_FILE, tasks)
    print("✅ Task added.")


def view_tasks(tasks, user):
    if not tasks[user]:
        print("📭 No tasks found.")
        return

    for i, task in enumerate(tasks[user], start=1):
        status = "✔ Done" if task["completed"] else "⏳ Pending"
        print(f"""
Task #{i}
Title     : {task['title']}
Priority  : {task['priority']}
Deadline  : {task['deadline']}
Status    : {status}
""")


def complete_task(tasks, user):
    view_tasks(tasks, user)
    try:
        index = int(input("Enter task number to mark complete: ")) - 1
        tasks[user][index]["completed"] = True
        save_data(TASKS_FILE, tasks)
        print("✅ Task marked as completed.")
    except:
        print("❌ Invalid selection.")


def delete_task(tasks, user):
    view_tasks(tasks, user)
    try:
        index = int(input("Enter task number to delete: ")) - 1
        removed = tasks[user].pop(index)
        save_data(TASKS_FILE, tasks)
        print(f"🗑 Deleted task: {removed['title']}")
    except:
        print("❌ Invalid selection.")


def task_stats(tasks, user):
    total = len(tasks[user])
    completed = sum(1 for t in tasks[user] if t["completed"])
    pending = total - completed

    print("\n📊 Task Statistics")
    print(f"Total     : {total}")
    print(f"Completed : {completed}")
    print(f"Pending   : {pending}")


# ------------------ MENUS ------------------

def task_menu(user):
    tasks = load_data(TASKS_FILE)
    if user not in tasks:
        tasks[user] = []

    while True:
        print("""
======== TASK MENU ========
1. Add Task
2. View Tasks
3. Complete Task
4. Delete Task
5. Task Statistics
6. Logout
===========================
""")
        choice = input("Choose: ")

        if choice == "1":
            add_task(tasks, user)
        elif choice == "2":
            view_tasks(tasks, user)
        elif choice == "3":
            complete_task(tasks, user)
        elif choice == "4":
            delete_task(tasks, user)
        elif choice == "5":
            task_stats(tasks, user)
        elif choice == "6":
            print("👋 Logged out.")
            break
        else:
            print("❌ Invalid option.")


def main():
    users = load_data(USERS_FILE)

    while True:
        print("""
===== PERSONAL TASK MANAGER =====
1. Register
2. Login
3. Exit
================================
""")
        choice = input("Choose: ")

        if choice == "1":
            user = register_user(users)
            if user:
                task_menu(user)
        elif choice == "2":
            user = login_user(users)
            if user:
                task_menu(user)
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option.")


if __name__ == "__main__":
    main()
