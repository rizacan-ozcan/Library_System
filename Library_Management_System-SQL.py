import sqlite3


class Book:
    def __init__(self, title, author, publisher, publish_year):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.publish_year = publish_year
        
    def show_info(self):
        print(50 * "#")
        print(f"""Book Information
              Title : {self.title}
              Author : {self.author}
              Publisher : {self.publisher}
              Publish Year : {self.publish_year}
              """)


class Member:
    def __init__(self, name, surname, member_number):
        self.name = name
        self.surname = surname
        self.member_number = member_number
        
    def show_info(self):
        print(50 * "*")
        print(f"""Member Information
              Name : {self.name}
              Surname : {self.surname}
              Member Number : {self.member_number}
              """)


class Library:
    def __init__(self):
        self.connect = sqlite3.connect("library.db")
        self.cursor = self.connect.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS BOOKS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                TITLE VARCHAR(300),
                AUTHOR VARCHAR(100),
                PUBLISHER VARCHAR(200),
                PUBLISH_YEAR DATE
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS MEMBERS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME VARCHAR(100),
                SURNAME VARCHAR(100),
                MEMBER_NUMBER VARCHAR(11)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS BORROWEDBOOKS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                BOOK_ID INTEGER,
                MEMBER_ID INTEGER,
                FOREIGN KEY (BOOK_ID) REFERENCES BOOKS (ID),
                FOREIGN KEY (MEMBER_ID) REFERENCES MEMBERS (ID)
            )
        ''')

        self.connect.commit()

    def _get_book_id(self, title):
        self.cursor.execute('SELECT ID FROM BOOKS WHERE TITLE = ?', (title,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def _get_member_id(self, member_number):
        self.cursor.execute('SELECT ID FROM MEMBERS WHERE MEMBER_NUMBER = ?', (member_number,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def add_book(self, book):
        self.cursor.execute('INSERT INTO BOOKS(TITLE, AUTHOR, PUBLISHER, PUBLISH_YEAR) VALUES(?, ?, ?, ?)', (book.title, book.author, book.publisher, book.publish_year))
        self.connect.commit()
        print(f"{book.title} has been added to the system.")

    def delete_book(self, title):
        book_id = self._get_book_id(title)
        if book_id:
            self.cursor.execute('DELETE FROM BOOKS WHERE ID = ?', (book_id,))
            self.connect.commit()
            print(f"{title} named book has been removed from the system.")
        else:
            print("You have entered a wrong book title, please try again.")

    def add_member(self, member):
        self.cursor.execute('INSERT INTO MEMBERS(NAME, SURNAME, MEMBER_NUMBER) VALUES(?, ?, ?)', (member.name, member.surname, member.member_number))
        self.connect.commit()
        print(f"{name} {surname} has been added to your system.")

    def delete_member(self, member_number):
        member_id = self._get_member_id(member_number)
        if member_id:
            self.cursor.execute('DELETE FROM MEMBERS WHERE MEMBER_NUMBER = ?', (member_id,))
            self.connect.commit()
            print(f"{member_number} has been deleted from your system.")
        else:
            print("You have entered a wrong member number, please try again.")

    def borrow_book(self, title, member_number):
        book_id = self._get_book_id(title)
        member_id = self._get_member_id(member_number)
        if book_id and member_id:
            self.cursor.execute('SELECT * FROM BORROWEDBOOKS WHERE BOOK_ID = ?', (book_id,))
            borrowed_status = self.cursor.fetchone()
            if borrowed_status:
                print(f"{title} has already been borrowed.")
            else:
                self.cursor.execute('INSERT INTO BORROWEDBOOKS(BOOK_ID, MEMBER_ID) VALUES(?, ?)', (book_id, member_id))
                self.connect.commit()
                print(f"{title} has been borrowed by {member_number}.")
        else:
            print("You have entered a wrong title or member number.")

    def return_book(self, title):
        book_id = self._get_book_id(title)
        if book_id:
            self.cursor.execute('SELECT * FROM BORROWEDBOOKS WHERE BOOK_ID = ?', (book_id,))
            borrowed_status = self.cursor.fetchone()
            if borrowed_status:
                self.cursor.execute('DELETE FROM BORROWEDBOOKS WHERE BOOK_ID = ?', (book_id,))
                self.connect.commit()
                print(f"{title} named book has been returned.")
            else:
                print(f"{title} named book has been not borrowed.")
        else:
            print("You have entered a wrong title or member number.")

    def show_books(self):
        self.cursor.execute('SELECT * FROM BOOKS')
        books = self.cursor.fetchall()
        if not books:
            print("Your library is empty, add books and try again.")
        else:
            print("\nBooks: ")
            for book in books:
                book_obj = Book(*book[1:])
                book_obj.show_info()

    def show_members(self):
        self.cursor.execute('SELECT * FROM MEMBERS')
        members = self.cursor.fetchall()
        if not members:
            print("Your member list is empty, please add and try again.")
        else:
            print("\nMembers: ")
            for member in members:
                member_obj = Member(*member[1:])
                member_obj.show_info()

    def close_connection(self):
        self.connect.close()


library = Library()


while True:
    print(20 * "*", "Library Management System", 20 * "*")
    print("""
            1. Add Book
            2. Delete Book
            3. Add Member
            4. Delete Member
            5. Borrow Book
            6. Return Book
            7. Show Book List
            8. Show Member List
            9. Exit
    """)
    
    action = input("Enter the action you wanted to perform: ")
    if action == "1":
        title = input("Title: ")
        author = input("Author: ")
        publisher = input("Publisher: ")
        publish_year = input("Publish Year: ")
        book = Book(title, author, publisher, publish_year)
        library.add_book(book)
    elif action == "2":
        title = input("Enter the title of the book you wanted to delete: ")
        library.delete_book(title)
    elif action == "3":
        name = input("Name: ")
        surname = input("Surname: ")
        member_number = input("Member Number: ")
        member = Member(name, surname, member_number)
        library.add_member(member)
    elif action == "4":
        member_number = input("Enter the number of the member you wanted to delete: ")
        library.delete_member(member_number)
    elif action == "5":
        title = input("Title: ")
        member_number = input("Member Number: ")
        library.borrow_book(title, member_number)

    elif action == "6":
        title = input("Title: ")
        library.return_book(title)

    elif action == "7":
        library.show_books()
    elif action == "8":
        library.show_members()
    elif action == "9" or action == "q" or action == "Q":
        print("You are exiting the system.")
        break
    else:
        print("You have entered a wrong input, please enter a correct one.")

library.close_connection()
