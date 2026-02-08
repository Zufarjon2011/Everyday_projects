class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True

    def borrow(self):
        if self.available:
            self.available = False
            return True
        return False

    def return_book(self):
        self.available = True

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "available": self.available
        }

    @staticmethod
    def from_dict(data):
        book = Book(data["title"], data["author"])
        book.available = data["available"]
        return book
