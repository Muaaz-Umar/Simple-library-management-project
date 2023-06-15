import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import date, timedelta


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="library2"
)

cursor = db.cursor()
# Queries for create table
create_books_table = "CREATE TABLE IF NOT EXISTS books (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), author VARCHAR(255), genre VARCHAR(255), publication_year INT)"
# create_members_table = "CREATE TABLE IF NOT EXISTS members (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), contact VARCHAR(255), membership_id VARCHAR(255), membership_type VARCHAR(255))"
create_borrow_table = "CREATE TABLE IF NOT EXISTS borrowings (id INT AUTO_INCREMENT PRIMARY KEY, book_id INT, member_id INT, borrow_date DATE, return_date DATE, returned BOOLEAN DEFAULT 0, fine DECIMAL(10,2) DEFAULT 0)"
# create_reservation_table = "CREATE TABLE IF NOT EXISTS reservations (id INT AUTO_INCREMENT PRIMARY KEY, book_id INT, member_id INT, reservation_date DATE, available BOOLEAN DEFAULT 0)"
create_user_table = "CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))"
create_faculty_table = "CREATE TABLE IF NOT EXISTS faculty (id INT PRIMARY KEY, emp_name VARCHAR(255), password VARCHAR(255))"
create_admin_table = "CREATE TABLE IF NOT EXISTS admins (id INT PRIMARY KEY, admin_name VARCHAR(255), password VARCHAR(255))"

cursor.execute(create_user_table)
cursor.execute(create_faculty_table)
cursor.execute(create_admin_table)
cursor.execute(create_books_table)
cursor.execute(create_borrow_table)


# globalization

user = ['student', 'faculty']

# function prototyping


def librarian_main_screen():
    pass


def student_main_screen():
    pass


def book_registration():
    # Create a new window for book registration
    book_registration_window = tk.Toplevel(root)
    book_registration_window.title("Book Registration")

    # Book Registration Labels and Entry Fields
    title_label = tk.Label(book_registration_window, text="Title")
    title_entry = tk.Entry(book_registration_window)
    author_label = tk.Label(book_registration_window, text="Author")
    author_entry = tk.Entry(book_registration_window)
    genre_label = tk.Label(book_registration_window, text="Genre")
    genre_entry = tk.Entry(book_registration_window)
    publication_year_label = tk.Label(
        book_registration_window, text="Publication Year")
    publication_year_entry = tk.Entry(book_registration_window)

    # Book Registration Button
    register_button = tk.Button(
        book_registration_window,
        text="Register Book",
        command=lambda: register_book(
            title_entry.get(),
            author_entry.get(),
            genre_entry.get(),
            publication_year_entry.get()
        )
    )

    # Positioning of Labels and Entry Fields
    title_label.grid(row=0, column=0, padx=5, pady=5)
    title_entry.grid(row=0, column=1, padx=5, pady=5)
    author_label.grid(row=1, column=0, padx=5, pady=5)
    author_entry.grid(row=1, column=1, padx=5, pady=5)
    genre_label.grid(row=2, column=0, padx=5, pady=5)
    genre_entry.grid(row=2, column=1, padx=5, pady=5)
    publication_year_label.grid(row=3, column=0, padx=5, pady=5)
    publication_year_entry.grid(row=3, column=1, padx=5, pady=5)
    register_button.grid(row=4, columnspan=2, padx=5, pady=5)


def register_book(title, author, genre, publication_year):
    # Insert the book into the database
    cursor.execute(
        "INSERT INTO books (title, author, genre, publication_year) VALUES (%s, %s, %s, %s)",
        (title, author, genre, publication_year)
    )
    db.commit()
    messagebox.showinfo("Success", "Book registration successful!")
    librarian_main_screen()


def book_viewing():
    # Create a new window for book viewing
    book_viewing_window = tk.Toplevel(root)
    book_viewing_window.title("Book Viewing")

    # Create a scrollbar for the book list
    scrollbar = tk.Scrollbar(book_viewing_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a listbox to display the book list
    book_listbox = tk.Listbox(
        book_viewing_window, yscrollcommand=scrollbar.set)
    book_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configure the scrollbar to work with the listbox
    scrollbar.config(command=book_listbox.yview)

    # Get all the books from the database
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    # Display the books in the listbox
    for book in books:
        book_listbox.insert(tk.END, f"{book[0]} - {book[1]} by {book[2]}")


def students_viewing():
    # Create a new window for students viewing
    students_viewing_window = tk.Toplevel(root)
    students_viewing_window.title("Students Viewing")

    # Create a scrollbar for the student list
    scrollbar = tk.Scrollbar(students_viewing_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a listbox to display the student list
    student_listbox = tk.Listbox(
        students_viewing_window, yscrollcommand=scrollbar.set)
    student_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    # Configure the scrollbar to work with the listbox
    scrollbar.config(command=student_listbox.yview)

    # Get all the students from the database
    cursor.execute("SELECT * FROM users")
    students = cursor.fetchall()

    # Display the students in the listbox
    for student in students:
        student_listbox.insert(tk.END, f"{student[0]} - {student[1]}")


def book_borrowing(usertype):
    # Create a new window for book borrowing
    book_borrowing_window = tk.Toplevel(root)
    book_borrowing_window.title("Book Borrowing")

    # Book Borrowing Labels and Entry Fields
    book_id_label = tk.Label(book_borrowing_window, text="Book ID")
    book_id_entry = tk.Entry(book_borrowing_window)
    user_id_label = tk.Label(book_borrowing_window, text="User ID")
    user_id_entry = tk.Entry(book_borrowing_window)

    # Book Borrowing Button
    borrow_button = tk.Button(
        book_borrowing_window,
        text="Borrow Book",
        command=lambda: borrow_book(
            book_id_entry.get(), user_id_entry.get(), usertype)
    )

    # Positioning of Labels and Entry Fields
    book_id_label.grid(row=0, column=0, padx=5, pady=5)
    book_id_entry.grid(row=0, column=1, padx=5, pady=5)
    user_id_label.grid(row=1, column=0, padx=5, pady=5)
    user_id_entry.grid(row=1, column=1, padx=5, pady=5)
    borrow_button.grid(row=2, columnspan=2, padx=5, pady=5)


def borrow_book(book_id, user_id, usertype):
    if not book_id:
        messagebox.showerror("Error", "Please enter a book ID.")
        return

    if not user_id:
        messagebox.showerror("Error", "Please enter a user ID.")
        return

    # Check if the book exists in the database
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()

    if book:
        # Check if the user exists in the database
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        if user:
            # Get the user type (student, faculty, librarian)
            user_type = usertype

            # Check if the user has reached the maximum borrowing limit based on user type
            if user_type == "student" and get_student_borrowed_count(int(user_id)) >= 2:
                messagebox.showerror(
                    "Error", "Maximum borrowing limit reached for students.")
            elif user_type == "faculty" and get_faculty_borrowed_count(int(user_id)) >= 4:
                messagebox.showerror(
                    "Error", "Maximum borrowing limit reached for faculty.")
            else:
                # Insert the borrowing record into the database
                if usertype == 'student':
                    cursor.execute(
                        "INSERT INTO borrowings (book_id, member_id, borrow_date, return_date) VALUES (%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY))",
                        (book_id, user_id)
                    )
                    db.commit()
                    messagebox.showinfo(
                        "Success", "Book borrowing successful!")
                if usertype == 'faculty':
                    cursor.execute(
                        "INSERT INTO borrowings (book_id, member_id, borrow_date, return_date) VALUES (%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY))",
                        (book_id, user_id)
                    )
                    db.commit()
                    messagebox.showinfo(
                        "Success", "Book borrowing successful!")

        else:
            messagebox.showerror("Error", "Invalid user ID.")
    else:
        messagebox.showerror("Error", "Invalid book ID.")


def get_student_borrowed_count(user_id):
    # Get the count of books borrowed by the student
    cursor.execute(
        "SELECT COUNT(*) FROM borrowings WHERE member_id = %s", (user_id,))
    result = cursor.fetchone()
    count = result[0]
    if count:
        return count
    else:
        return 0


def get_faculty_borrowed_count(user_id):
    # Get the count of books borrowed by the faculty
    cursor.execute(
        "SELECT COUNT(*) FROM borrowings WHERE member_id = %s", (user_id,))
    result = cursor.fetchone()
    count = result[0]
    if count:
        return count
    else:
        return 0


def borrowed_book_viewing_user(user_id):
    # Create a new window for book viewing
    book_viewing_window = tk.Toplevel(root)
    book_viewing_window.title("Borrowed Book Viewing")

    # Create a scrollbar for the book list
    scrollbar = tk.Scrollbar(book_viewing_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a listbox to display the book list
    book_listbox = tk.Listbox(
        book_viewing_window, yscrollcommand=scrollbar.set)
    book_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configure the scrollbar to work with the listbox
    scrollbar.config(command=book_listbox.yview)

    # Get all the books from the database
    cursor.execute("SELECT books.title FROM borrowings JOIN books ON borrowings.book_id = books.id WHERE borrowings.member_id = %s AND borrowings.returned = 0", (user_id,))
    books = cursor.fetchall()

    # Display the books in the listbox
    for book in books:
        book_listbox.insert(tk.END, book[0])


def admin_view_borrowed_books():
    # Create a new window for viewing borrowed books
    view_window = tk.Toplevel(root)
    view_window.title("Borrowed Books")

    # Retrieve all borrowed books from the database
    cursor.execute("SELECT users.id, users.username, books.title FROM borrowings JOIN users ON borrowings.member_id = users.id JOIN books ON borrowings.book_id = books.id WHERE borrowings.returned = 0")
    borrowed_books = cursor.fetchall()

    # Display borrowed books in the window
    if borrowed_books:
        for i, borrowed_book in enumerate(borrowed_books):
            user_id = borrowed_book[0]
            user_name = borrowed_book[1]
            book_title = borrowed_book[2]

            book_label = tk.Label(
                view_window, text=f"Book {i+1}: {book_title}")
            id_label = tk.Label(view_window, text=f"User ID: {user_id}")
            name_label = tk.Label(view_window, text=f"User Name: {user_name}")
            book_label.pack()

            id_label.pack()
            name_label.pack()
    else:
        no_books_label = tk.Label(view_window, text="No borrowed books.")
        no_books_label.pack()


def calculate_faculty_fine(borrow_date, return_date):
    fine_rate = 70  # Fine rate per day in RS
    max_fine_days = 37  # Maximum days for fine calculation

    # Calculate the number of days between borrow and return dates
    duration = return_date - borrow_date
    days = duration.days
    print(days)

    # Calculate the fine amount
    if days > 30:
        if days <= max_fine_days:
            fine_amount = (days-30) * fine_rate
        else:
            fine_amount = (max_fine_days-30) * fine_rate

    else:
        fine_amount = 0
    return fine_amount


def calculate_student_fine(borrow_date, return_date):
    fine_rate = 50  # Fine rate per day in RS
    max_fine_days = 21  # Maximum days for fine calculation

    # Calculate the number of days between borrow and return dates
    duration = return_date - borrow_date
    days = duration.days
    print(days)

    # Calculate the fine amount
    if days > 14:
        if days <= max_fine_days:
            fine_amount = (days-14) * fine_rate
        else:
            fine_amount = (max_fine_days-14) * fine_rate

    else:
        fine_amount = 0
    return fine_amount


def fine_calculation(user_type, user_id):
    # Create a new window for fine calculation and display
    fine_window = tk.Toplevel(root)
    fine_window.title("Fine Calculation")

    # Get borrowed books and calculate fines
    cursor.execute("SELECT books.title, borrowings.borrow_date, borrowings.return_date FROM borrowings JOIN books ON borrowings.book_id = books.id WHERE borrowings.member_id = %s AND borrowings.returned = 0", (user_id,))
    borrowings = cursor.fetchall()

    # Display borrowed books and fines
    if borrowings:
        if user_type == 'student':
            for i, borrowing in enumerate(borrowings):
                title = borrowing[0]
                borrow_date = borrowing[1]
                return_date = borrowing[2]
                fine_amount = calculate_student_fine(borrow_date, return_date)
                book_label = tk.Label(fine_window, text=f"Book {i+1}: {title}")
                fine_label = tk.Label(
                    fine_window, text=f"Fine Amount: {fine_amount} RS")
                book_label.pack()
                fine_label.pack()
        if user_type == 'faculty':
            for i, borrowing in enumerate(borrowings):
                title = borrowing[0]
                borrow_date = borrowing[1]
                return_date = borrowing[2]
                fine_amount = calculate_faculty_fine(borrow_date, return_date)
                book_label = tk.Label(fine_window, text=f"Book {i+1}: {title}")
                fine_label = tk.Label(
                    fine_window, text=f"Fine Amount: {fine_amount} RS")
                book_label.pack()
                fine_label.pack()

    else:
        no_books_label = tk.Label(fine_window, text="No borrowed books.")
        no_books_label.pack()


root = tk.Tk()
root.title("Library Management System")
root.geometry('500x500')


def destroy_all_widgets():
    # Destroy all widgets present on the main window
    for widget in root.winfo_children():
        widget.destroy()


def librarian_main_screen():
    destroy_all_widgets()

    add_book_button = tk.Button(
        root, text='Add book', command=book_registration)
    add_book_button.pack()
    # Add book_viewing button to the main screen
    book_viewing_button = tk.Button(
        root, text="View Books", command=book_viewing)
    book_viewing_button.pack()
    # Add students_viewing button to the main screen
    students_viewing_button = tk.Button(
        root, text="Students Viewing", command=students_viewing)
    students_viewing_button.pack()

    borrow_book_view_all_button = tk.Button(
        root, text='View All borrowed books', command=admin_view_borrowed_books)
    borrow_book_view_all_button.pack()

    signup_button = tk.Button(root, text='Signup', command=signup)
    signup_button.pack()

    logout_button = tk.Button(root, text='Log out', command=login)
    logout_button.pack()


def student_main_screen(user_id):
    destroy_all_widgets()
    usertype = 'student'
    userid = user_id
    # Add book_viewing button to the main screen
    book_viewing_button = tk.Button(
        root, text="View Books", command=book_viewing)
    book_viewing_button.pack()
    # Add book_borrowing button to the main screen
    book_borrowing_button = tk.Button(
        root, text="Borrow Book", command=lambda: book_borrowing(usertype=user[0]))
    book_borrowing_button.pack()

    borrowed_books_button = tk.Button(
        root, text="View Borrowed Books", command=lambda: borrowed_book_viewing_user(user_id))
    borrowed_books_button.pack()

    calculate_fine_button = tk.Button(
        root, text='Calculate Fine', command=lambda: fine_calculation(usertype, userid))
    calculate_fine_button.pack()

    logout_button = tk.Button(root, text='Log out', command=login)
    logout_button.pack()


def faculty_main_screen(user_id):
    destroy_all_widgets()
    usertype = 'faculty'
    userid = user_id
    # Add book_viewing button to the main screen
    book_viewing_button = tk.Button(
        root, text="View Books", command=book_viewing)
    book_viewing_button.pack()
    # Add book_borrowing button to the main screen
    book_borrowing_button = tk.Button(
        root, text="Borrow Book", command=lambda: book_borrowing(usertype=user[1]))
    book_borrowing_button.pack()

    borrowed_books_button = tk.Button(
        root, text="View Borrowed Books", command=lambda: borrowed_book_viewing_user(user_id))
    borrowed_books_button.pack()

    calculate_fine_button = tk.Button(
        root, text='Calculate Fine', command=lambda: fine_calculation(usertype, userid))
    calculate_fine_button.pack()

    logout_button = tk.Button(root, text='Log out', command=login)
    logout_button.pack()


def login():
    destroy_all_widgets()

    username_entry_lable = tk.Label(root, text='Username entry')
    username_entry_lable.pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    password_entry_lable = tk.Label(root, text='Password entry')
    password_entry_lable.pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    login_user_button = tk.Button(root, text='Login as student', command=lambda: login_user(
        username_entry.get(), password_entry.get()))
    login_user_button.pack()
    faculty_login_button = tk.Button(root, text='Login as faculty', command=lambda: login_faculty(
        username_entry.get(), password_entry.get()))
    faculty_login_button.pack()
    librarian_login_button = tk.Button(root, text='Login as librarian', command=lambda: login_librarian(
        username_entry.get(), password_entry.get()))
    librarian_login_button.pack()


def login_user(username, password):
    # Check if the entered credentials exist in the database
    cursor.execute(
        "SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    if user:
        user_id = user[0]

    if user:
        messagebox.showinfo("Success", "Login successful!")
        student_main_screen(user_id)
    else:
        messagebox.showerror("Error", "Invalid username or password.")


def login_faculty(username, password):
    # Check if the entered credentials exist in the database
    cursor.execute(
        "SELECT * FROM faculty WHERE emp_name = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    if user:
        user_id = user[0]

    if user:
        messagebox.showinfo("Success", "Login successful!")
        faculty_main_screen(user_id)
    else:
        messagebox.showerror("Error", "Invalid username or password.")


def login_librarian(username, password):
    # Check if the entered credentials exist in the database
    cursor.execute(
        "SELECT * FROM admins WHERE admin_name = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Success", "Login successful!")
        librarian_main_screen()

    else:
        messagebox.showerror("Error", "Invalid username or password.")


def signup():
    destroy_all_widgets()
    user_signup_button = tk.Button(
        root, text='Signup as student', command=student_signup)
    user_signup_button.pack()
    employee_signup_button = tk.Button(
        root, text='Signup as faculty', command=faculty_signup)
    employee_signup_button.pack()
    faculty_signup_button = tk.Button(
        root, text='Signup as librarian', command=librarian_signup)
    faculty_signup_button.pack()


def student_signup():
    destroy_all_widgets()

    student_roll_label = tk.Label(root, text="Student ID:")
    student_roll_label.grid(row=0, column=0, sticky="e")
    student_roll_entry = tk.Entry(root)
    student_roll_entry.grid(row=0, column=1, pady=5)

    student_name_label = tk.Label(root, text="Student Name:")
    student_name_label.grid(row=1, column=0, sticky="e")
    student_name_entry = tk.Entry(root)
    student_name_entry.grid(row=1, column=1, pady=5)

    student_password_label = tk.Label(root, text="Password")
    student_password_label.grid(row=2, column=0, sticky="e")
    student_password_entry = tk.Entry(root, show="*")
    student_password_entry.grid(row=2, column=1, pady=5)

    student_confirm_password_label = tk.Label(root, text="Confirm Password:")
    student_confirm_password_label.grid(row=3, column=0, sticky="e")
    student_confirm_password_entry = tk.Entry(root, show="*")
    student_confirm_password_entry.grid(row=3, column=1, pady=5)

    def validate_student_signup():
        student_id_val = student_roll_entry.get()
        student_name_val = student_name_entry.get()
        student_password_val = student_password_entry.get()
        student_confirm_password_val = student_confirm_password_entry.get()

        if not student_id_val or not student_name_val or not student_password_val or not student_confirm_password_val:
            messagebox.showerror("Error", "Please fill in all fields")
        elif student_password_val != student_password_val:
            messagebox.showerror("Error", "Passwords do not match")
        else:
            sql = "INSERT INTO users (id ,username, password) VALUES (%s, %s, %s)"
            values = (student_id_val, student_name_val, student_password_val)

            cursor.execute(sql, values)
            db.commit()

            messagebox.showinfo("Success", "Account created successfully")
            login()
    student_signup_button = tk.Button(
        root, text='Signup', command=validate_student_signup)
    student_signup_button.grid(row=4, column=0, sticky="e")


def faculty_signup():
    destroy_all_widgets()

    employee_id_label = tk.Label(root, text="Employee ID:")
    employee_id_label.grid(row=0, column=0, sticky="e")
    employee_id_entry = tk.Entry(root)
    employee_id_entry.grid(row=0, column=1, pady=5)

    employee_name_label = tk.Label(root, text="Employee Name:")
    employee_name_label.grid(row=1, column=0, sticky="e")
    employee_name_entry = tk.Entry(root)
    employee_name_entry.grid(row=1, column=1, pady=5)

    employee_password_label = tk.Label(root, text="Password:")
    employee_password_label.grid(row=2, column=0, sticky="e")
    employee_password_entry = tk.Entry(root, show="*")
    employee_password_entry.grid(row=2, column=1, pady=5)

    employee_confirm_password_label = tk.Label(root, text="Confirm Password:")
    employee_confirm_password_label.grid(row=3, column=0, sticky="e")
    employee_confirm_password_entry = tk.Entry(root, show="*")
    employee_confirm_password_entry.grid(row=3, column=1, pady=5)

    def validate_faculty_librarian_signup():
        employee_id_val = employee_id_entry.get()
        employee_name_val = employee_name_entry.get()
        employee_password_val = employee_password_entry.get()
        employee_confirm_password_val = employee_confirm_password_entry.get()

        if not employee_id_val or not employee_name_val or not employee_password_val or not employee_confirm_password_val:
            messagebox.showerror("Error", "Please fill in all fields")
        elif employee_password_val != employee_confirm_password_val:
            messagebox.showerror("Error", "Passwords do not match")
        else:
            sql = "INSERT INTO faculty (id, emp_name, password) VALUES (%s, %s, %s)"
            values = (employee_id_val, employee_name_val,
                      employee_password_val)

            cursor.execute(sql, values)
            db.commit()

            messagebox.showinfo("Success", "Account created successfully")
            login()

    faculty_signup_button = tk.Button(
        root, text='Signup', command=validate_faculty_librarian_signup)
    faculty_signup_button.grid(row=4, column=0, sticky="e")


def librarian_signup():
    destroy_all_widgets()

    employee_id_label = tk.Label(root, text="Employee ID:")
    employee_id_label.grid(row=0, column=0, sticky="e")
    employee_id_entry = tk.Entry(root)
    employee_id_entry.grid(row=0, column=1, pady=5)

    employee_name_label = tk.Label(root, text="Employee Name:")
    employee_name_label.grid(row=1, column=0, sticky="e")
    employee_name_entry = tk.Entry(root)
    employee_name_entry.grid(row=1, column=1, pady=5)

    employee_password_label = tk.Label(root, text="Password:")
    employee_password_label.grid(row=2, column=0, sticky="e")
    employee_password_entry = tk.Entry(root, show="*")
    employee_password_entry.grid(row=2, column=1, pady=5)

    employee_confirm_password_label = tk.Label(root, text="Confirm Password:")
    employee_confirm_password_label.grid(row=3, column=0, sticky="e")
    employee_confirm_password_entry = tk.Entry(root, show="*")
    employee_confirm_password_entry.grid(row=3, column=1, pady=5)

    def validate_librarian_signup():
        employee_id_val = employee_id_entry.get()
        employee_name_val = employee_name_entry.get()
        employee_password_val = employee_password_entry.get()
        employee_confirm_password_val = employee_confirm_password_entry.get()

        if not employee_id_val or not employee_name_val or not employee_password_val or not employee_confirm_password_val:
            messagebox.showerror("Error", "Please fill in all fields")
        elif employee_password_val != employee_confirm_password_val:
            messagebox.showerror("Error", "Passwords do not match")
        else:
            sql = "INSERT INTO admins (id, admin_name, password) VALUES (%s, %s, %s)"
            values = (employee_id_val, employee_name_val,
                      employee_password_val)

            cursor.execute(sql, values)
            db.commit()

            messagebox.showinfo("Success", "Account created successfully")
            login()

    faculty_signup_button = tk.Button(
        root, text='Signup', command=validate_librarian_signup)
    faculty_signup_button.grid(row=4, column=0, sticky="e")


login()
root.mainloop()
