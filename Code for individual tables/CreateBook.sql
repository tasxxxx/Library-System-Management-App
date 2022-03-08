CREATE TABLE Book(
	accessionNo     VARCHAR(5)  NOT NULL, 
    title           VARCHAR(80) NOT NULL,
    isbn            VARCHAR(80) NOT NULL,
    publisher       VARCHAR(80) NOT NULL, 
    publicationYear INT         NOT NULL,
    PRIMARY KEY (accessionNo)
    );