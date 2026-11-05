#Creating two files books and users to store information of books and users respectively
BOOKS_FILE = "books.txt"
USERS_FILE = "users.txt"

#class book
class Book:
    def __init__(self, bookid, title, author, borrowed_by=""):
        self.__bookid = bookid
        self.__title = title
        self.__author = author
        self.__borrowed_by = borrowed_by

    def get_bookid(self):
        return self.__bookid

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_borrowed_by(self):
        return self.__borrowed_by

    def is_available(self):
        return self.__borrowed_by == ""

    def borrow(self, user_id):
        self.__borrowed_by = user_id

    def give_back(self):
        self.__borrowed_by = ""

    def show(self):
        if self.is_available():
            status = "Available"
        else:
            status = "Borrowed by " + self.__borrowed_by
        print("Bookid:",self.__bookid + "  " + "Title:", self.__title + "  " + "Author:", self.__author +"  "+"Status:",  status)


#class user
class User:
    def __init__(self, user_id, name):
        self.__user_id = user_id
        self.__name = name
        self.__books = []          
        self.max_books = 1         

    def get_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def get_books(self):
        return self.__books

    def get_type(self):
        return "User"

    def can_borrow(self):
        return len(self.__books) < self.max_books

    def add_book(self, bookid):
        self.__books.append(bookid)

    def remove_book(self, bookid):
        self.__books.remove(bookid)

    def show(self):
        print("Userid:",self.__user_id + "  " +"Name:", self.__name + "  " +"Type:", self.get_type() +
              " Borrowed:" + str(len(self.__books)) + "/" + str(self.max_books))


#inheritance
class Student(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.max_books = 3         #students can borrow a max of 3 books

    def get_type(self):
        return "Student"


class Staff(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.max_books = 10        #staff can borrow a max of 10 books

    def get_type(self):
        return "Staff"


#library class
class Library:
    def __init__(self):
        self.books = {}    #book dictionary to store books information
        self.users = {}    #user dictionary to store user information
        self.load()

    #writing files
    def save(self):
        file = open(BOOKS_FILE, "w")
        for book in self.books.values():
            file.write(book.get_bookid() + "|" + book.get_title() + "|" +
                       book.get_author() + "|" + book.get_borrowed_by() + "\n")
        file.close()

        file = open(USERS_FILE, "w")
        for user in self.users.values():
            borrowed = ",".join(user.get_books())
            file.write(user.get_type() + "|" + user.get_id() + "|" +
                       user.get_name() + "|" + borrowed + "\n")
        file.close()

    def load(self):
        try:
            file = open(BOOKS_FILE, "r")
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 4:
                    self.books[parts[0]] = Book(parts[0], parts[1], parts[2], parts[3])
            file.close()
        except FileNotFoundError:
            #adding sample books
            self.books["101"] = Book("101", "To Kill a Mockingbird", "Harper Lee")
            self.books["102"] = Book("102", "Harry Potter", "JK Rowling")
            self.books["103"] = Book("103", "The Lord of Rings", "JRR Tolkien")

        try:
            file = open(USERS_FILE, "r")
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 4:
                    if parts[0] == "Student":
                        user = Student(parts[1], parts[2])
                    else:
                        user = Staff(parts[1], parts[2])
                    if parts[3] != "":
                        for bookid in parts[3].split(","):
                            user.add_book(bookid)
                    self.users[parts[1]] = user
            file.close()
        except FileNotFoundError:
            pass

    #fuctions
    def register(self, user_type, user_id, name):
        if user_id in self.users:
            print("ID already used; use another")
            return
        if user_type == "1":
            self.users[user_id] = Student(user_id, name)
        else:
            self.users[user_id] = Staff(user_id, name)
        self.save()
        print("User registered!")

    def add_book(self, bookid, title, author):
        if bookid in self.books:
            print("That bookid already exists ")
            return
        self.books[bookid] = Book(bookid, title, author)
        self.save()
        print("Book successfully added!!!")

    def borrow(self, user_id, bookid):
        if user_id not in self.users:
            print("User not found ")
        elif bookid not in self.books:
            print("Book not found ")
        elif not self.books[bookid].is_available():
            print("Sorry, that book is already borrowed ")
        elif not self.users[user_id].can_borrow():
            print("You have reached your borrowing limit ")
        else:
            self.books[bookid].borrow(user_id)
            self.users[user_id].add_book(bookid)
            self.save()
            print("You borrowed " + self.books[bookid].get_title())

    def return_book(self, user_id, bookid):
        if user_id not in self.users:
            print("User not found ")
        elif bookid not in self.books:
            print("Book not found ")
        elif self.books[bookid].get_borrowed_by() != user_id:
            print("This user did not borrow that book ")
        else:
            self.books[bookid].give_back()
            self.users[user_id].remove_book(bookid)
            self.save()
            print("Book returned. Thank you!")

    def search(self, word):
        word = word.lower()
        found = False
        for book in self.books.values():
            if word in book.get_title().lower() or word in book.get_author().lower():
                book.show()
                found = True
        if not found:
            print("No books found ")

    def show_all_books(self):
        for book in self.books.values():
            book.show()

    def show_all_users(self):
        if len(self.users) == 0:
            print("No users found ")
        for user in self.users.values():
            user.show()


#Main program
def main():
    library = Library()

    while True:
        print()
        print("**********LIBRARY MENU**********")
        print("Press 1 to register a new user")
        print("Press 2 to add a book")
        print("Press 3 to borrow book")
        print("Press 4 to return book")
        print("Press 5 to search books")
        print("Press 6 to show all books")
        print("Press 7 to show all users")
        print("Press 0 to exit")
        print()
        choice = input("Please choose an option: ")

        if choice == "1":
            print("1. Student   2. Staff")
            user_type = input("Type: ")
            user_id = input("ID: ")
            name = input("Name: ")
            library.register(user_type, user_id, name)
        elif choice == "2":
            bookid = input("BookID: ")
            title = input("Title: ")
            author = input("Author: ")
            library.add_book(bookid, title, author)
        elif choice == "3":
            user_id = input("Your ID: ")
            bookid = input("BookId: ")
            library.borrow(user_id, bookid)
        elif choice == "4":
            user_id = input("Your ID: ")
            bookid = input("Bookid: ")
            library.return_book(user_id, bookid)
        elif choice == "5":
            library.search(input("Search title or author: "))
        elif choice == "6":
            library.show_all_books()
        elif choice == "7":
            library.show_all_users()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


main()