CREATE TABLE RESERVATION(
	accessionNo         VARCHAR(5)  NOT NULL,
    reserveDate         DATE        NOT NULL,
    reservationMemberId VARCHAR(45) NOT NULL, 
    PRIMARY KEY(accessionNo),
    FOREIGN KEY(accessionNo) REFERENCES Book(accessionNo) ON DELETE CASCADE,
    FOREIGN KEY(reservationMemberId) REFERENCES Members(memberId) ON DELETE CASCADE
    );

