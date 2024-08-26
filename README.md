# Library Management System
## Overview
A Python-based Library Management System using MS SQL Server for managing books, members, transactions, and more. This project includes features for efficient library management and record-keeping.

## Features
* Books Management: Add, update, and delete book records.
* Members Management: Manage library members' details.
* Transactions Management: Track book borrowings and returns.
* Reservations Management: Handle book reservations.
* Fines Management: Record and manage fines.
* Reviews Management: Add and manage book reviews.
* Notifications Management: Manage notifications to users.
* Activity Log: Log user actions for auditing.
## Database Schema
* Books: BookID, Title, Quantity, CategoryID, Author, PublicationYear
Members: MemberID, Name
* Transactions: TransactionID, BookID, MemberID, Status, TransactionDate, DueDate, ReturnDate
Categories: CategoryID, CategoryName
* Reservations: ReservationID, BookID, MemberID, ReservationDate, Status
Fines: FineID, TransactionID, Amount, Paid
* Reviews: ReviewID, BookID, MemberID, Rating, ReviewText
* Notifications: NotificationID, UserID, Message, Sent, SentDate
* ActivityLog: LogID, UserID, Action, ActionDate
## Setup
1-Database: Create the BOOK_Library database and execute the SQL scripts to set up tables.
2- Python Environment: Install dependencies with pip install pypyodbc.
3-Configuration: Update connection details in the DatabaseConnection class.
4- Running: Execute the Python script to interact with the system.
