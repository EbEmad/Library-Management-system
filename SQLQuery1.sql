-- Step 1: Create Users Table for Authentication and Roles
CREATE TABLE Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    Username NVARCHAR(255) NOT NULL UNIQUE,
    PasswordHash NVARCHAR(255) NOT NULL,
    Role NVARCHAR(50) NOT NULL  -- 'Admin', 'Librarian', 'Member'
);

-- Step 2: Create Categories Table for Book Categories
CREATE TABLE Categories (
    CategoryID INT IDENTITY(1,1) PRIMARY KEY,
    CategoryName NVARCHAR(100) NOT NULL
);

-- Step 3: Create Books Table
CREATE TABLE Books (
    BookID INT IDENTITY(1,1) PRIMARY KEY,
    Title NVARCHAR(255) NOT NULL,
    Quantity INT NOT NULL,
    CategoryID INT FOREIGN KEY REFERENCES Categories(CategoryID),
    Author NVARCHAR(255),
    PublicationYear INT
);

-- Step 4: Create Members Table
CREATE TABLE Members (
    MemberID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(255) NOT NULL
);

-- Step 5: Create Transactions Table
CREATE TABLE Transactions (
    TransactionID INT IDENTITY(1,1) PRIMARY KEY,
    BookID INT FOREIGN KEY REFERENCES Books(BookID),
    MemberID INT FOREIGN KEY REFERENCES Members(MemberID),
    Status NVARCHAR(50) NOT NULL,   -- 'borrowed', 'returned'
    TransactionDate DATE DEFAULT GETDATE(),
    DueDate DATE,
    ReturnDate DATE
);

-- Step 6: Create Reservations Table for Book Reservations
CREATE TABLE Reservations (
    ReservationID INT IDENTITY(1,1) PRIMARY KEY,
    BookID INT FOREIGN KEY REFERENCES Books(BookID),
    MemberID INT FOREIGN KEY REFERENCES Members(MemberID),
    ReservationDate DATE NOT NULL,
    Status NVARCHAR(50) NOT NULL DEFAULT 'pending'  -- 'pending', 'fulfilled'
);

-- Step 7: Create Fines Table for Managing Fines
CREATE TABLE Fines (
    FineID INT IDENTITY(1,1) PRIMARY KEY,
    TransactionID INT FOREIGN KEY REFERENCES Transactions(TransactionID),
    Amount DECIMAL(10, 2) NOT NULL,
    Paid BIT DEFAULT 0
);

-- Step 8: Create Reviews Table for Book Ratings and Reviews
CREATE TABLE Reviews (
    ReviewID INT IDENTITY(1,1) PRIMARY KEY,
    BookID INT FOREIGN KEY REFERENCES Books(BookID),
    MemberID INT FOREIGN KEY REFERENCES Members(MemberID),
    Rating INT CHECK (Rating >= 1 AND Rating <= 5),
    ReviewText NVARCHAR(MAX)
);

-- Step 9: Create Notifications Table for User Notifications
CREATE TABLE Notifications (
    NotificationID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT FOREIGN KEY REFERENCES Users(UserID),
    Message NVARCHAR(255) NOT NULL,
    Sent BIT DEFAULT 0,
    SentDate DATE
);

-- Step 10: Create Activity Log Table for Tracking User Actions
CREATE TABLE ActivityLog (
    LogID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT FOREIGN KEY REFERENCES Users(UserID),
    Action NVARCHAR(255) NOT NULL,
    ActionDate DATETIME DEFAULT GETDATE()
);
