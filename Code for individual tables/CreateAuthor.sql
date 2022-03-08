CREATE TABLE AUTHOR(
	accessionNo 	VARCHAR(5)  NOT NULL,
    author      	VARCHAR(45) NOT NULL,
    PRIMARY KEY(accessionNo, author),
    FOREIGN KEY(accessionNo) REFERENCES Book(accessionNo) ON DELETE CASCADE
    );

