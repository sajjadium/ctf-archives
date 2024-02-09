#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rich.console import Console
import re
import shlex
import os

FLAG = os.getenv("FLAG","FAKE_FLAG") 

console=Console()
class Member:
    def __init__(self, name):
        self.name = name

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

class BookCopy:
    def __init__(self, book):
        self.book = book
        self.available = True

class SaveFile:
    def __init__(self, file_name=os.urandom(16).hex()):
        self.file = file_name

class Library:
    def __init__(self, name):
        self.name = name
        self.books = {}
        self.members = {}

    def add_book(self, book, num_copies=1):
        if book.isbn in self.books:
            self.books[book.isbn] += num_copies
        else:
            self.books[book.isbn] = num_copies

    def add_member(self, member):
        self.members[member.name] = member

    def display_books(self,title=''):
        if not title == '':
            for isbn, num_copies in self.books.items():
                book = isbn_to_book[isbn]
                if book.title == title:
                    return book.title
                else:
                    console.print("\n[bold red]Book not found.[/bold red]")
        else:
            console.print(f"\n[bold green]Books in {self.name} Library:[/bold green]")
            for isbn, num_copies in self.books.items():
                book = isbn_to_book[isbn]
                status = f"{num_copies} copies available" if num_copies > 0 else "All copies checked out"
                console.print(f"[cyan]ISBN: {isbn} - Status: {status}[/cyan]")

    def search_book(self):
        pattern = console.input("[bold blue]Enter the pattern to search: [/bold blue]")
        matching_books = []
        for isbn, num_copies in self.books.items():
            book = isbn_to_book[isbn]
            if re.fullmatch(pattern,book.title):
                matching_books.append(book)

        if matching_books:
            console.print(f"\n[bold yellow]Found matching books for '{pattern}':[bold yellow]")
            for book in matching_books:
                status = f"{num_copies} copies available" if num_copies > 0 else "All copies checked out"
                console.print(f"[cyan]ISBN: {book.isbn} - Status: {status}[/cyan]")
        else:
            console.print(f"[bold yellow]No matching books found for '{pattern}'.[/bold yellow]")

    def check_out_book(self, isbn, member_name):
        if member_name not in self.members:
            console.print(f"\n[bold red]Member '{member_name}' not found.[/bold red]")
            return

        if isbn not in isbn_to_book:
            console.print("\n[bold red]Book not found.[/bold red]")
            return

        if isbn not in self.books or self.books[isbn] <= 0:
            console.print("\n[bold red]All copies of the book are currently checked out.[/bold red]")
            return

        member = self.members[member_name]
        book_copy = BookCopy(isbn_to_book[isbn])

        for i in range(len(member_books.setdefault(member_name, []))):
            if member_books[member_name][i].book.isbn == isbn and member_books[member_name][i].available:
                member_books[member_name][i] = book_copy
                self.books[isbn] -= 1
                console.print(f"\n[bold green]Successfully checked out:[/bold green] [cyan]{book_copy.book} for {member.name}[/cyan]")
                return

        console.print("\n[bold red]No available copies of the book for checkout.[/bold red]")

    def return_book(self, isbn, member_name):
        if member_name not in self.members:
            console.print(f"\n[bold red]Member '{member_name}' not found.[/bold red]")
            return

        if isbn not in isbn_to_book:
            console.print("\n[bold red]Book not found.[/bold red]")
            return

        member = self.members[member_name]

        for i in range(len(member_books.setdefault(member_name, []))):
            if member_books[member_name][i].book.isbn == isbn and not member_books[member_name][i].available:
                member_books[member_name][i].available = True
                self.books[isbn] += 1
                console.print(f"\n[bold green]Successfully returned:[/bold green] [cyan]{member_books[member_name][i].book} by {member.name}[/cyan]")
                return

        console.print("\n[bold red]Book not checked out to the member or already returned.[/bold red]")


def save_book(title, content='zAbuQasem'):
    try:
        with open(title, 'w') as file:
            file.write(content)
        console.print(f"[bold green]Book saved successfully[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")

def check_file_presence():
    book_name = shlex.quote(console.input("[bold blue]Enter the name of the book (file) to check:[/bold blue] "))
    command = "ls " + book_name

    try:
        result = os.popen(command).read().strip()
        print(result)
        if result == book_name:
            console.print(f"[bold green]The book is present in the current directory.[/bold green]")
        else:
            console.print(f"[bold red]The book is not found in the current directory.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")

if __name__ == "__main__":
    library = Library("My Library")
    isbn_to_book = {}
    member_books = {}
    while True:
        console.print("\n[bold blue]Library Management System[/bold blue]")
        console.print("1. Add Member")
        console.print("2. Add Book")
        console.print("3. Display Books")
        console.print("4. Search Book")
        console.print("5. Check Out Book")
        console.print("6. Return Book")
        console.print("7. Save Book")
        console.print("8. Check File Presence")
        console.print("0. Exit")

        choice = console.input("[bold blue]Enter your choice (0-8): [/bold blue]")

        if choice == "0":
            console.print("[bold blue]Exiting Library Management System. Goodbye![/bold blue]")
            break
        elif choice == "1":
            member_name = console.input("[bold blue]Enter member name: [/bold blue]")
            library.add_member(Member(member_name))
            console.print(f"[bold green]Member '{member_name}' added successfully.[/bold green]")
        elif choice == "2":
            title = console.input("[bold blue]Enter book title: [/bold blue]").strip()
            author = console.input("[bold blue]Enter book author: [/bold blue]")
            isbn = console.input("[bold blue]Enter book ISBN: [/bold blue]")
            num_copies = int(console.input("[bold blue]Enter number of copies: [/bold blue]"))
            book = Book(title, author, isbn)
            isbn_to_book[isbn] = book
            library.add_book(book, num_copies)
            console.print(f"[bold green]Book '{title}' added successfully with {num_copies} copies.[/bold green]")
        elif choice == "3":
            library.display_books()
        elif choice == "4":
            library.search_book()
        elif choice == "5":
            isbn = console.input("[bold blue]Enter ISBN of the book: [/bold blue]")
            member_name = console.input("[bold blue]Enter member name: [/bold blue]")
            library.check_out_book(isbn, member_name)
        elif choice == "6":
            isbn = console.input("[bold blue]Enter ISBN of the book: [/bold blue]")
            member_name = console.input("[bold blue]Enter member name: [/bold blue]")
            library.return_book(isbn, member_name)
        elif choice == "7":
            choice = console.input("\n[bold blue]Book Manager:[/bold blue]\n1. Save Existing\n2. Create new book\n[bold blue]Enter your choice (1-2): [/bold blue]")
            if choice == "1":
                title = console.input("[bold blue]Enter Book title to save: [/bold blue]").strip()
                file = SaveFile(library.display_books(title=title))
                save_book(file.file, content="Hello World")
            else:
                save_file = SaveFile()
                title = console.input("[bold blue]Enter book title: [/bold blue]").strip()
                author = console.input("[bold blue]Enter book author: [/bold blue]")
                isbn = console.input("[bold blue]Enter book ISBN: [/bold blue]")
                num_copies = int(console.input("[bold blue]Enter number of copies: [/bold blue]"))
                title = title.format(file=save_file)
                book = Book(title,author, isbn)
                isbn_to_book[isbn] = book
                library.add_book(book, num_copies)
                save_book(title)
        elif choice == "8":
            check_file_presence()
        else:
            console.print("[bold red]Invalid choice. Please enter a number between 0 and 8.[/bold red]")