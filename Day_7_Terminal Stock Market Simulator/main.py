import json
import os
import random
from datetime import datetime

DATA_FILE = "market_data.json"

INITIAL_BALANCE = 10000

STOCKS = {
    "TECH": 150.0,
    "AUTO": 80.0,
    "ENERGY": 60.0,
    "AI": 200.0,
    "FOOD": 40.0
}


# ----------------- DATA -----------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "balance": INITIAL_BALANCE,
            "portfolio": {},
            "history": [],
            "prices": STOCKS
        }

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ----------------- MARKET LOGIC -----------------

def update_market(data):
    for stock in data["prices"]:
        change_percent = random.uniform(-5, 5)
        old_price = data["prices"][stock]
        new_price = round(old_price * (1 + change_percent / 100), 2)
        data["prices"][stock] = max(new_price, 1)


def show_market(data):
    print("\n=== MARKET PRICES ===")
    for stock, price in data["prices"].items():
        print(f"{stock}: ${price}")


# ----------------- TRADING -----------------

def buy_stock(data):
    show_market(data)
    stock = input("Stock symbol to buy: ").upper()

    if stock not in data["prices"]:
        print("Invalid stock.")
        return

    quantity = int(input("Quantity: "))
    cost = data["prices"][stock] * quantity

    if cost > data["balance"]:
        print("Insufficient balance.")
        return

    data["balance"] -= cost
    data["portfolio"][stock] = data["portfolio"].get(stock, 0) + quantity

    data["history"].append({
        "type": "BUY",
        "stock": stock,
        "quantity": quantity,
        "price": data["prices"][stock],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    save_data(data)
    print("Stock purchased.")


def sell_stock(data):
    if not data["portfolio"]:
        print("No stocks owned.")
        return

    stock = input("Stock symbol to sell: ").upper()

    if stock not in data["portfolio"]:
        print("You don't own this stock.")
        return

    quantity = int(input("Quantity: "))

    if quantity > data["portfolio"][stock]:
        print("Not enough shares.")
        return

    revenue = data["prices"][stock] * quantity
    data["balance"] += revenue
    data["portfolio"][stock] -= quantity

    if data["portfolio"][stock] == 0:
        del data["portfolio"][stock]

    data["history"].append({
        "type": "SELL",
        "stock": stock,
        "quantity": quantity,
        "price": data["prices"][stock],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    save_data(data)
    print("Stock sold.")


# ----------------- PORTFOLIO -----------------

def show_portfolio(data):
    print("\n=== PORTFOLIO ===")
    print(f"Balance: ${round(data['balance'], 2)}")

    total_value = data["balance"]

    for stock, quantity in data["portfolio"].items():
        current_price = data["prices"][stock]
        value = current_price * quantity
        total_value += value
        print(f"{stock} - {quantity} shares | Current value: ${round(value, 2)}")

    print(f"\nTotal Net Worth: ${round(total_value, 2)}")


# ----------------- MENU -----------------

def menu():
    print("\n=== STOCK MARKET SIMULATOR ===")
    print("1. View Market")
    print("2. Update Market (Next Day)")
    print("3. Buy Stock")
    print("4. Sell Stock")
    print("5. View Portfolio")
    print("6. Exit")


def main():
    data = load_data()

    while True:
        menu()
        choice = input("Choose option: ")

        if choice == "1":
            show_market(data)
        elif choice == "2":
            update_market(data)
            save_data(data)
            print("Market updated.")
        elif choice == "3":
            buy_stock(data)
        elif choice == "4":
            sell_stock(data)
        elif choice == "5":
            show_portfolio(data)
        elif choice == "6":
            print("Exiting market.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
