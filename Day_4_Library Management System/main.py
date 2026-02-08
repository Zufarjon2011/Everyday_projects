from models import Book
from storage import load_books, save_books


def menu():
    print("\n=== LIBRARY MANAGEMENT SYSTEM ===")
    print("1. Add Book")
    print("2. Borrow Book")
    print("3. Return Book")
    print("4. Show All Books")
    print("5. Exit")


def show_books(books):
    if not books:
        print("No books in library.")
        return

    for i, book in enumerate(books, 1):
        status = "Available" if book.available else "Borrowed"
        print(f"{i}. {book.title} by {book.author} [{status}]")


def main():
    books = load_books()

    while True:
        menu()
        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Book title: ")
            author = input("Author: ")
            books.append(Book(title, author))
            save_books(books)
            print("Book added.")

        elif choice == "2":
            show_books(books)
            idx = int(input("Book number to borrow: ")) - 1
            if books[idx].borrow():
                save_books(books)
                print("Book borrowed.")
            else:
                print("Book already borrowed.")

        elif choice == "3":
            show_books(books)
            idx = int(input("Book number to return: ")) - 1
            books[idx].return_book()
            save_books(books)
            print("Book returned.")

        elif choice == "4":
            show_books(books)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
