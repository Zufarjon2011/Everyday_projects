import json
import os
from datetime import datetime, timedelta

DATA_FILE = "tasks_data.json"


class Task:
    def __init__(self, title, priority, deadline):
        self.title = title
        self.priority = priority  # Low / Medium / High
        self.deadline = deadline
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.completed_at = None

    def to_dict(self):
        return {
            "title": self.title,
            "priority": self.priority,
            "deadline": self.deadline,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }


class StudySession:
    def __init__(self, task_title, minutes):
        self.task_title = task_title
        self.minutes = minutes
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "task_title": self.task_title,
            "minutes": self.minutes,
            "date": self.date
        }


class TaskPlanner:
    def __init__(self):
        self.tasks = []
        self.study_sessions = []
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.tasks = data.get("tasks", [])
                self.study_sessions = data.get("sessions", [])
        else:
            self.tasks = []
            self.study_sessions = []

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump({
                "tasks": self.tasks,
                "sessions": self.study_sessions
            }, f, indent=4)

    def add_task(self, title, priority, deadline):
        task = Task(title, priority, deadline)
        self.tasks.append(task.to_dict())
        self.save_data()

    def complete_task(self, index):
        try:
            self.tasks[index]["completed"] = True
            self.tasks[index]["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_data()
        except IndexError:
            print("Invalid task number.")

    def add_study_session(self, task_title, minutes):
        session = StudySession(task_title, minutes)
        self.study_sessions.append(session.to_dict())
        self.save_data()

    def overdue_tasks(self):
        now = datetime.now()
        overdue = []

        for task in self.tasks:
            if not task["completed"]:
                deadline = datetime.strptime(task["deadline"], "%Y-%m-%d")
                if deadline < now:
                    overdue.append(task)

        return overdue

    def show_tasks(self):
        if not self.tasks:
            print("No tasks available.")
            return

        for i, task in enumerate(self.tasks, 1):
            status = "✓" if task["completed"] else "✗"
            print(f"{i}. [{status}] {task['title']} | Priority: {task['priority']} | Deadline: {task['deadline']}")

    def study_statistics(self):
        total_minutes = sum(s["minutes"] for s in self.study_sessions)
        return total_minutes


def menu():
    print("\n==== SMART TASK & STUDY PLANNER ====")
    print("1. Add Task")
    print("2. Complete Task")
    print("3. Show Tasks")
    print("4. Add Study Session")
    print("5. Overdue Tasks")
    print("6. Study Statistics")
    print("7. Exit")


def main():
    planner = TaskPlanner()

    while True:
        menu()
        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Task title: ")
            priority = input("Priority (Low/Medium/High): ")
            deadline = input("Deadline (YYYY-MM-DD): ")
            planner.add_task(title, priority, deadline)
            print("Task added.")

        elif choice == "2":
            planner.show_tasks()
            index = int(input("Task number to complete: ")) - 1
            planner.complete_task(index)
            print("Task marked as completed.")

        elif choice == "3":
            planner.show_tasks()

        elif choice == "4":
            task_title = input("Task title: ")
            minutes = int(input("Study minutes: "))
            planner.add_study_session(task_title, minutes)
            print("Study session recorded.")

        elif choice == "5":
            overdue = planner.overdue_tasks()
            if not overdue:
                print("No overdue tasks 🎉")
            else:
                print("Overdue tasks:")
                for task in overdue:
                    print(f"- {task['title']} (Deadline: {task['deadline']})")

        elif choice == "6":
            total = planner.study_statistics()
            print(f"Total study time: {total} minutes")

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
