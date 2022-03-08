CREATE TABLE Due (
    borrowDate DATE  NOT NULL,
    dueDate    DATE  NOT NULL,
    PRIMARY KEY(borrowDate),
    FOREIGN KEY(borrowDate) REFERENCES Borrow(borrowDate)
    );