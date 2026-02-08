import json
import os
from models import Book

DATA_FILE = "library_data.json"


def load_books():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        return [Book.from_dict(b) for b in data]


def save_books(books):
    with open(DATA_FILE, "w") as f:
        json.dump([b.to_dict() for b in books], f, indent=4)
