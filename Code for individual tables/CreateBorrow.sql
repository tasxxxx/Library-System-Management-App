CREATE TABLE Borrow (
    accessionNo    VARCHAR(5)   NOT NULL,
    borrowDate     DATE         NOT NULL,
    borrowMemberId VARCHAR(45)  NOT NULL,
    returnDate     DATE,
    PRIMARY KEY(accessionNo, borrowDate),
    FOREIGN KEY(accessionNo) REFERENCES Book(accessionNo) ON DELETE CASCADE,
    FOREIGN KEY(borrowMemberId) REFERENCES Members(memberId) ON DELETE CASCADE
    );
    

    

