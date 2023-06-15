# Software Requirements Specification (SRS) for Library Management System

## 1. Introduction

The Library Management System is a software application designed to automate and streamline the operations of a library. It provides a user-friendly interface for librarians, faculty members, and students to manage books, borrowing, fines, and more.

## 2. Functional Requirements

### 2.1. User Management

- The system shall allow users to create an account with appropriate user types: librarian, faculty member, or student.
- The system shall authenticate users during login and provide access based on user type.

### 2.2. Book Registration

- Librarians shall be able to register new books by entering details such as title, author, genre, and publication year.
- Each book shall be assigned a unique identifier (e.g., ISBN) for easy identification and retrieval.

### 2.3. Book Borrowing and Returning

- Users shall be able to borrow books by entering the book's identifier (ISBN) and their respective user ID.
- For students, the system shall set a borrowing duration of 2 weeks and a maximum of 2 books.
- For faculty members, the system shall set a borrowing duration of 1 month and a maximum of 4 books.
- Users shall be able to return borrowed books, updating the status in the system.

### 2.4. Fines and Payments

- The system shall calculate fines for late submission of borrowed books based on a predefined fine rate per day.
- The fine rate shall be set at 50 RS per day.
- Fines shall not increase after 7 days.
- Users shall be able to make payments for fines through the system.

## 3. Non-Functional Requirements

### 3.1. User Interface

- The system shall have an intuitive and user-friendly interface for easy navigation and usage.
- The interface shall be responsive and compatible with various screen sizes and devices.

### 3.2. Performance

- The system shall be capable of handling a large number of concurrent users without significant performance degradation.
- Response times for critical operations shall be within acceptable limits.

### 3.3. Security

- User passwords shall be securely stored using appropriate hashing algorithms.
- Access to sensitive data and operations shall be restricted based on user types and authentication.

## 4. Constraints

- The system shall be developed using Python programming language.
- The backend database shall be MySQL.
- The frontend shall be implemented using the Tkinter library for GUI.

## 5. Assumptions

- Users have access to a computer or device with internet connectivity.
- Users have basic computer literacy skills to interact with the system.

## 6. Dependencies

- The system depends on the availability and proper functioning of the MySQL database.
- Proper network connectivity is required for users to access the system.

## 7. References

- [Library Management System Project Proposal](https://github.com/Muaaz-Umar/Simple-library-management-project)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [MySQL Documentation](https://dev.mysql.com/doc/connector-python/en/)
