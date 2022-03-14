
CREATE DATABASE Library;

CREATE TABLE Members(
	memberId   VARCHAR(45)  NOT NULL, 
    memberName VARCHAR(45)  NOT NULL,
    faculty    VARCHAR(45)  NOT NULL, 
    phoneNo    INT          NOT NULL, 
    emailAdd   VARCHAR(100) NOT NULL,
    PRIMARY KEY (memberId)
    ); 
    
CREATE TABLE Book(
	accessionNo     VARCHAR(5)  NOT NULL, 
    title           VARCHAR(80) NOT NULL,
    isbn            VARCHAR(80) NOT NULL,
    publisher       VARCHAR(80) NOT NULL, 
    publicationYear INT         NOT NULL,
    PRIMARY KEY (accessionNo)
    );
    
CREATE TABLE Fine(
	memberId    VARCHAR(45) NOT NULL,
    fineAmount  INT         NOT NULL, 
    PRIMARY KEY(memberId), 
    FOREIGN KEY(memberId) REFERENCES Members(memberId) ON DELETE CASCADE
    );

CREATE TABLE Author(
	accessionNo 	VARCHAR(5)  NOT NULL,
    author      	VARCHAR(45) NOT NULL,
    PRIMARY KEY(accessionNo, author),
    FOREIGN KEY(accessionNo) REFERENCES Book(accessionNo) ON DELETE CASCADE
    );
    
CREATE TABLE Reservation(
	accessionNo         VARCHAR(5)  NOT NULL,
    reserveDate         DATE        NOT NULL,
    reservationMemberId VARCHAR(45) NOT NULL, 
    PRIMARY KEY(accessionNo),
    FOREIGN KEY(accessionNo) REFERENCES Book(accessionNo) ON DELETE CASCADE,
    FOREIGN KEY(reservationMemberId) REFERENCES Members(memberId) ON DELETE CASCADE
    );

CREATE TABLE Borrow (
    accessionNo    VARCHAR(5)   NOT NULL,
    borrowDate     DATE         NOT NULL,
    borrowMemberId VARCHAR(45)  NOT NULL,
    returnDate     DATE,
    PRIMARY KEY(accessionNo, borrowDate),
    FOREIGN KEY(accessionNo) REFERENCES Book(accessionNo) ON DELETE CASCADE,
    FOREIGN KEY(borrowMemberId) REFERENCES Members(memberId) ON DELETE CASCADE
    );

CREATE TABLE Payment(
	memberId    VARCHAR(45) NOT NULL,
    paymentDate DATE        NOT NULL, 
    PRIMARY KEY(memberId, paymentDate), 
    FOREIGN KEY(memberId) REFERENCES Members(memberId) ON DELETE CASCADE
    );