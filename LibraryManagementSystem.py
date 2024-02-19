class Member:
    def __init__(self, name_surname, mem_number, depart):
        self.name_surname = name_surname
        self.mem_number = mem_number
        self.depart = depart

    def show_info(self):
        print("\nMember Information")
        print(f"""
        Name and Surname: {self.name_surname}
        Member Number: {self.mem_number}
        Department: {self.depart}
        """)

class Book:
    def __init__(self, title, author, page_number, pub_year):
        self.title = title
        self.author = author
        self.page_number = page_number
        self.pub_year = pub_year

    def show_info(self):
        print("\nBook Information")
        print(f"""
        Title: {self.title}
        Author: {self.author}
        Publish Year: {self.pub_year}
        Page Number: {self.page_number}
        """)

class Library:
    def __init__(self):
        self.members = []
        self.books = []
        self.borrowed_books = {}

    def add_member(self, member):
        self.members.append(member)
        print(f"{member.name_surname} has been successfully added to the system.")

    def delete_member(self, mem_number):
        for member in self.members:
            if mem_number == member.mem_number:
                self.members.remove(member)
                print(f"{member.name_surname} has been successfully removed from the system.")
            else:
                print("The member number you have given is incorrect")

    def add_book(self, book):
        self.books.append(book)
        print(f"{book.title} has been successfully added to the system.")

    def remove_book(self, title):
        for book in self.books:
            if title == book.title:
                self.books.remove(book)
                print(f"{book.title} has been successfully removed from the system.")
            else:
                print("The title you have given is incorrect.")

    def show_members(self):
        if len(self.members) == 0:
            print("There is not any member registered.")
        else:
            print("\nAll Members: ")
            for member in self.members:
                member.show_info()

    def show_books(self):
        if len(self.books) == 0:
            print("There is not any book registered.")
        else:
            print("\nAll Books: ")
            for book in self.books:
                book.show_info()

    def borrow_book(self, book, member):
        if book in self.books and member in self.members:
            if book not in self.borrowed_books:
                self.borrowed_books[book] =  member
                print(f"{book.title} is successfully borrowed by {member.name_surname}.")
            else:
                print("The book title or number you have given is incorrect.")

    def return_book(self, book):
        if book in self.borrowed_books:
            member = self.borrowed_books.pop(book)
            print(f"{book.title} is successfully returned by {member.name_surname}.")
        else:
            print("The title you have given is not in the borrowed books list.")


library = Library()

while True:
    print(20 * "*", "Library System", 20 * "*")
    print("""
    1. Add Member
    2. Delete Member
    3. Add Book
    4. Delete Book
    5. Borrow Book
    6. Return Book
    7. Show Members
    8. Show Books
    9. Exit(q-Q)
    """)
    action = input("")

    if action == "1":
        name_surname = input("Enter your name and surname: ")
        mem_number = input("Enter your member number: ")
        depart = input("Enter your department: ")
        member = Member(name_surname, mem_number, depart)
        library.add_member(member)

    elif action == "2":
        mem_number = input("Enter the member number you want to delete: ")
        library.delete_member(mem_number)

    elif action == "3":
        title = input("Enter title: ")
        author = input("Enter author: ")
        page_number = input("Enter page number: ")
        pub_year = input("Enter publish year: ")
        book = Book(title, author, page_number, pub_year)
        library.add_book(book)

    elif action == "4":
        title = input("Enter the book title you want to delete: ")
        library.remove_book(title)

    elif action == "5":
        title = input("Which book do you want to borrow ? ")
        mem_number = input(f"Who will borrow {title}(Enter a member number!) ? ")
        book = next((a for a in library.books if title == a.title), None)
        member = next((b for b in library.members if mem_number == b.mem_number), None)
        if book and member:
            library.borrow_book(book, member)
        else:
            print(f"The number or title you have given is either incorrect or {title} is currently borrowed")

    elif action == "6":
        title = input("Which book do you want to return ? ")
        book = next((f for f in library.books if title == f.title), None)
        if book:
            library.return_book(book)
        else:
            print("The title you have entered is either incorrect or not borrowed.")

    elif action == "7":
        library.show_members()

    elif action == "8":
        library.show_books()

    elif action == "9" or action == "q" or action == "Q":
        print("You are exiting the system")
        break

    else:
        print("You have entered an incorrect action.")