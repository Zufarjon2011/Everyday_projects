import json
import os
from datetime import datetime

DATA_FILE = "finance_data.json"


class Transaction:
    def __init__(self, amount, category, description, t_type):
        self.amount = amount
        self.category = category
        self.description = description
        self.type = t_type  # income or expense
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "type": self.type,
            "date": self.date
        }


class FinanceManager:
    def __init__(self):
        self.transactions = []
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.transactions = data
        else:
            self.transactions = []

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.transactions, f, indent=4)

    def add_income(self, amount, category, description):
        t = Transaction(amount, category, description, "income")
        self.transactions.append(t.to_dict())
        self.save_data()

    def add_expense(self, amount, category, description):
        t = Transaction(amount, category, description, "expense")
        self.transactions.append(t.to_dict())
        self.save_data()

    def get_balance(self):
        balance = 0
        for t in self.transactions:
            if t["type"] == "income":
                balance += t["amount"]
            else:
                balance -= t["amount"]
        return balance

    def monthly_summary(self, month):
        income = 0
        expense = 0

        for t in self.transactions:
            if t["date"].startswith(month):
                if t["type"] == "income":
                    income += t["amount"]
                else:
                    expense += t["amount"]

        return income, expense

    def show_all_transactions(self):
        if not self.transactions:
            print("No transactions yet.")
            return

        for i, t in enumerate(self.transactions, 1):
            print(f"{i}. [{t['type'].upper()}] {t['amount']} | {t['category']} | {t['description']} | {t['date']}")


def menu():
    print("\n==== PERSONAL FINANCE MANAGER ====")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Balance")
    print("4. Monthly Summary")
    print("5. Show All Transactions")
    print("6. Exit")


def main():
    manager = FinanceManager()

    while True:
        menu()
        choice = input("Choose an option: ")

        if choice == "1":
            amount = float(input("Amount: "))
            category = input("Category: ")
            description = input("Description: ")
            manager.add_income(amount, category, description)
            print("Income added successfully.")

        elif choice == "2":
            amount = float(input("Amount: "))
            category = input("Category: ")
            description = input("Description: ")
            manager.add_expense(amount, category, description)
            print("Expense added successfully.")

        elif choice == "3":
            balance = manager.get_balance()
            print(f"Current Balance: {balance}")

        elif choice == "4":
            month = input("Enter month (YYYY-MM): ")
            income, expense = manager.monthly_summary(month)
            print(f"Income: {income}")
            print(f"Expense: {expense}")
            print(f"Net: {income - expense}")

        elif choice == "5":
            manager.show_all_transactions()

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
