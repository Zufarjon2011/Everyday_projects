import json
import os
import hashlib
import re
from getpass import getpass

DATA_FILE = "vault.json"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def password_strength(password):
    score = 0
    rules = [
        len(password) >= 8,
        re.search(r"[A-Z]", password),
        re.search(r"[a-z]", password),
        re.search(r"[0-9]", password),
        re.search(r"[!@#$%^&*()_+=\-]", password)
    ]
    score = sum(bool(rule) for rule in rules)

    if score <= 2:
        return "Weak"
    elif score == 3:
        return "Medium"
    elif score == 4:
        return "Strong"
    else:
        return "Very Strong"


def load_vault():
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_vault(vault):
    with open(DATA_FILE, "w") as f:
        json.dump(vault, f, indent=4)


def add_entry(vault):
    site = input("Website: ")
    username = input("Username: ")
    password = getpass("Password: ")

    strength = password_strength(password)
    print(f"Password strength: {strength}")

    if strength == "Weak":
        print("Password too weak. Entry not saved.")
        return

    vault[site] = {
        "username": username,
        "password_hash": hash_password(password)
    }
    save_vault(vault)
    print("Entry saved securely.")


def view_entries(vault):
    if not vault:
        print("Vault is empty.")
        return

    for site, data in vault.items():
        print(f"{site} -> {data['username']} (hashed)")


def menu():
    print("\n=== PASSWORD VAULT ===")
    print("1. Add Entry")
    print("2. View Entries")
    print("3. Exit")


def main():
    vault = load_vault()

    while True:
        menu()
        choice = input("Choose an option: ")

        if choice == "1":
            add_entry(vault)
        elif choice == "2":
            view_entries(vault)
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
