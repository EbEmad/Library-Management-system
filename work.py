import sys
import pypyodbc as odbc

# Connection details
DRIVER_NAME = 'SQL Server'
SERVER_NAME = 'LAPTOP-9547JE77\\EBEMAD24'
DATABASE_NAME = 'BOOK_Library'

conn_string = f"""
    Driver={{{DRIVER_NAME}}};
    Server={SERVER_NAME};
    Database={DATABASE_NAME};
    Trust_Connection=yes;
"""

class DatabaseConnection:
    def __init__(self):
        try:
            self.conn = odbc.connect(conn_string)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)
            print('Task terminated')
            sys.exit()

    def commit(self):
        try:
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)
            print('Transaction rolled back')

    def close(self):
        self.cursor.close()
        if self.conn.connected == 1:
            print('Connection closed')
            self.conn.close()

class BaseModel:
    def __init__(self, db, table_name, columns):
        self.db = db
        self.table_name = table_name
        self.columns = columns

    def insert(self, values):
        column_names = ', '.join(self.columns)
        placeholders = ', '.join(['?'] * len(values))
        insert_statement = f"INSERT INTO {self.table_name} ({column_names}) VALUES ({placeholders})"
        try:
            self.db.cursor.execute(insert_statement, values)
            self.db.commit()
            print(f'{self.table_name} record added successfully')
        except Exception as e:
            print(e)

    def update(self, update_values, where_values):
        set_clause = ', '.join([f"{col} = ?" for col in self.columns[:-1]])
        update_statement = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.columns[-1]} = ?"
        try:
            self.db.cursor.execute(update_statement, update_values + where_values)
            self.db.commit()
            print(f'{self.table_name} record updated successfully')
        except Exception as e:
            print(e)

    def delete(self, where_value):
        delete_statement = f"DELETE FROM {self.table_name} WHERE {self.columns[-1]} = ?"
        try:
            self.db.cursor.execute(delete_statement, [where_value])
            self.db.commit()
            print(f'{self.table_name} record deleted successfully')
        except Exception as e:
            print(e)

    def print_all(self):
        select_statement = f"SELECT * FROM {self.table_name}"
        try:
            self.db.cursor.execute(select_statement)
            rows = self.db.cursor.fetchall()
            print(f"{self.table_name} table data:")
            for row in rows:
                print(row)
        except Exception as e:
            print(e)

# Existing Tables
class Book(BaseModel):
    def __init__(self, db):
        super().__init__(db, 'Books', ['Title', 'Quantity', 'CategoryID', 'Author', 'PublicationYear'])

class Member(BaseModel):
    def __init__(self, db):
        super().__init__(db, 'Members', ['Name'])

class Transaction(BaseModel):
    def __init__(self, db):
        super().__init__(db, 'Transactions', ['BookID', 'MemberID', 'Status', 'TransactionDate', 'DueDate', 'ReturnDate'])

# New Tables
class User(BaseModel):
    def __init__(self, db):
        super().__init__(db, 'Users', ['Username', 'PasswordHash', 'Role'])

class Category(BaseModel):
    def __init__(self, db):
        super().__init__(db, 'Categories', ['CategoryName'])

class Reservation(BaseModel):
    def __init__(self, db):
        super().__init__(db, 'Reservations', ['BookID', 'MemberID', 'ReservationDate', 'Status'])

class Fine(BaseModel):
    def __init__(self, db):
        super().__init__(db, 'Fines', ['TransactionID', 'Amount', 'Paid'])

class Review(BaseModel):
    def __init__(self, db):
        super().__init__(db, 'Reviews', ['BookID', 'MemberID', 'Rating', 'ReviewText'])

class Notification(BaseModel):
    def __init__(self, db):
        super().__init__(db, 'Notifications', ['UserID', 'Message', 'Sent', 'SentDate'])

class ActivityLog(BaseModel):
    def __init__(self, db):
        super().__init__(db, 'ActivityLog', ['UserID', 'Action', 'ActionDate'])

# Main code
db = DatabaseConnection()

# Add a category
category = Category(db)
category.insert(['Science Fiction'])

# Add a book with CategoryID 1 (assuming this ID exists)
book = Book(db)
book.insert(['Machine Learning', 5, 1, 'John Doe', 2021])

# Add a member
member = Member(db)
member.insert(['Ali Hatem'])

# Add a transaction for the book and member
transaction = Transaction(db)
transaction.insert([1, 1, 'borrowed', '2024-08-26', '2024-09-02', None])

# Add a reservation for the existing book with valid BookID and MemberID
reservation = Reservation(db)
reservation.insert([1, 1, '2024-08-26', 'pending'])

# Add a fine for the existing transaction with valid TransactionID
fine = Fine(db)
fine.insert([1, 50.00, 0])  # Ensure TransactionID 1 exists

# Add a review for the existing book with valid BookID
review = Review(db)
review.insert([1, 1, 5, 'Great book!'])

# Add a notification
notification = Notification(db)
notification.insert([1, 'Your book is due soon', 0, '2024-08-25'])

# Log an activity
activity_log = ActivityLog(db)
activity_log.insert([1, 'Book borrowed', '2024-08-26'])

# Print data from a table
book.print_all()

# Close the connection
db.close()
