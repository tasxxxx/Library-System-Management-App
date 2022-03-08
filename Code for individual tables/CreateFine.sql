CREATE TABLE Fine(
	memberId    VARCHAR(45) NOT NULL,
    paymentDate DATE,
    fineAmount  INT         NOT NULL, 
    PRIMARY KEY(memberId, paymentDate), 
    FOREIGN KEY(memberId) REFERENCES Members(memberId) ON DELETE CASCADE
    );
