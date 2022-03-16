import sqlalchemy as db
from tkinter import *
from datetime import datetime
from datetime import timedelta
from datetime import date
import time

USERNAME = "root"
PASSWORD = "Hoepeng.0099"
HOST = "localhost"
PORT = 3306
DB = "Library"

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
cursor = engine.connect()

TITLE_FONT = ("Bahnschrift", 15)
DEFAULT_FONT = ("Bahnschrift", 11)

def loansBorrow():

    root = Tk()

    global accessionNo_field
    global membershipID_field

    toplabel = Label(root, text = "To Borrow a Book, Please Enter Information Below:", font = TITLE_FONT, bg = "#5AA9E6")
    toplabel.grid(row = 1, column = 2, sticky = NSEW)

    label1 = Label(root, text = "Accession Number", font = DEFAULT_FONT, bg = "#FFE45E")
    label1.grid(row = 2, column = 2)
    label2 = Label(root, text = "Membership ID", font = DEFAULT_FONT, bg = "#FFE45E")
    label2.grid(row = 3, column = 2)

    accessionNo_field = Entry(root, width = 30)
    accessionNo_field.grid(row = 2, column = 3, sticky = W)
    membershipID_field = Entry(root, width = 30)
    membershipID_field.grid(row = 3, column = 3, sticky = W)

    button1 = Button(root, text = "Borrow Book", font = DEFAULT_FONT, bg = "#5AA9E6", command = popup_window)
    button1.grid(row = 8, column = 2)
    button2 = Button(root, text = "Back to Loans Menu", font = DEFAULT_FONT, bg = "#5AA9E6", command = root.destroy)
    button2.grid(row = 8, column = 3)

    root.mainloop()

def loan_books():

    win = Tk()

    # Predicate: Whether book is on loan
    # Predicate: Whether book is on reservation 
    # Predicate: Whether member reached loan quota
    # Predicate: Whether member has outstanding fine
    sql1 = "SELECT * FROM Borrow WHERE (accessionNo = '{}' AND returnDate IS null)".format(accessionNo)
    on_loan = cursor.execute(sql1).fetchall()
    sql2 = "SELECT * FROM Reservation WHERE accessionNo = '{}' AND reservationMemberId != '{}'".format(accessionNo, membershipID)
    on_reservation = cursor.execute(sql2).fetchall()
    sql3 = "SELECT * FROM Borrow WHERE (borrowMemberId = '{}' AND returnDate IS null)".format(membershipID)
    books_borrowed = cursor.execute(sql3).fetchall()
    sql4 = "SELECT * FROM Fine WHERE memberId = '{}'".format(membershipID)
    member_fine = cursor.execute(sql4).fetchall()
    fineamt = 0
    
    if (len(member_fine) > 0):
        fineamt = member_fine[0][1]

    if (len(on_loan) > 0):
        # Error
        label1 = Label(win, text = "Error!", font = TITLE_FONT)
        label1.pack()
        old_due_date = cursor.execute(sql1).fetchall()[0][1] + timedelta(days = 14)
        label2 = Label(win, text = "Book is currently on Loan until: '{}'".format(old_due_date.strftime("%d/%m/%Y")), font = DEFAULT_FONT)
        label2.pack() 
        btn = Button(win, text = "Back to Borrow Function", font = DEFAULT_FONT, bg = "#5AA9E6", command = win.destroy)
        btn.pack()
    elif (len(on_reservation) > 0):
        # Error
        label1 = Label(win, text = "Error!", font = TITLE_FONT)
        label1.pack()
        label2 = Label(win, text = "Book is currently on Reservation", font = DEFAULT_FONT)
        label2.pack() 
        btn = Button(win, text = "Back to Borrow Function", font = DEFAULT_FONT, bg = "#5AA9E6", command = win.destroy)
        btn.pack()
    elif (len(books_borrowed) == 2):
        # Error
        label1 = Label(win, text = "Error!", font = TITLE_FONT)
        label1.pack()
        label2 = Label(win, text = "Member loan quota exceeded.", font = DEFAULT_FONT)
        label2.pack() 
        btn = Button(win, text = "Back to Borrow Function", font = DEFAULT_FONT, bg = "#5AA9E6", command = win.destroy)
        btn.pack()
    elif (fineamt > 0):
        # Error
        label1 = Label(win, text = "Error!", font = TITLE_FONT)
        label1.pack()
        label2 = Label(win, text = "Member has outstanding fine.", font = DEFAULT_FONT)
        label2.pack() 
        btn = Button(win, text = "Back to Borrow Function", font = DEFAULT_FONT, bg = "#5AA9E6", command = win.destroy)
        btn.pack()
    else:
        # Success
        label1 = Label(win, text = "Success!", font = TITLE_FONT)
        label1.pack()
        label2 = Label(win, text = "Book has been borrowed.", font = DEFAULT_FONT)
        label2.pack() 
        btn = Button(win, text = "Back to Borrow Function", font = DEFAULT_FONT, bg = "#5AA9E6", command = win.destroy)
        btn.pack()

        # INSERT DATA INTO BORROW
        sql5 = "INSERT INTO Borrow VALUES ('{}', '{}', '{}', null)".format(accessionNo, borrow_date, membershipID)
        cursor.execute(sql5)

        # DELETE DATA FROM RESERVATION IF LOANED TO RESERVED MEMBER
        sql6 = "SELECT * FROM Reservation WHERE accessionNo = '{}' AND reservationMemberId = '{}'".format(accessionNo, membershipID)
        reserved = cursor.execute(sql6).fetchall()

        if (len(reserved) > 0):
            cursor.execute("DELETE FROM Reservation WHERE accessionNo = '{}'".format(accessionNo))

    win.mainloop()

def popup_window():

    win = Tk()

    global accessionNo
    global membershipID
    global borrow_date
    accessionNo = accessionNo_field.get()
    membershipID = membershipID_field.get()

    # Predicate: Whether book is in database
    # Predicate: Whether member is in database
    sql01 = "SELECT * FROM Book WHERE accessionNo = '{}'".format(accessionNo)
    book_valid = cursor.execute(sql01).fetchall()
    sql02 = "SELECT * FROM Members WHERE (memberId = '{}')".format(membershipID)
    member_valid = cursor.execute(sql02).fetchall()
    
    if (len(book_valid) > 0 and len(member_valid) > 0):

        toplabel = Label(win, text = "Confirm Loan Details to Be Correct", font = TITLE_FONT)
        toplabel.grid(row = 1, column = 2, sticky = NSEW)
        get_query = "SELECT * FROM Book WHERE accessionNo = '{}'".format(accessionNo)
        get_member = "SELECT * FROM Members WHERE memberId = '{}'".format(membershipID)
        book_title = cursor.execute(get_query).fetchall()[0][1]
        datetimeobj1 = date.today()
        borrow_date = datetimeobj1.strftime("%Y/%m/%d")
        member_name = cursor.execute(get_member).fetchall()[0][1]
        datetimeobj2 = datetimeobj1 + timedelta(days = 14)
        due_date = datetimeobj2.strftime("%Y/%m/%d")

        label1 = Label(win, text = "Accession Number: '{}'".format(accessionNo), font = DEFAULT_FONT, bg = "#FFE45E")
        label1.grid(row = 2, column = 2, sticky = W)
        label2 = Label(win, text = "Book Title: '{}'".format(book_title), font = DEFAULT_FONT, bg = "#FFE45E")
        label2.grid(row = 3, column = 2, sticky = W)
        label3 = Label(win, text = "Borrow Date: '{}'".format(borrow_date), font = DEFAULT_FONT, bg = "#FFE45E")
        label3.grid(row = 4, column = 2, sticky = W)
        label4 = Label(win, text = "Membership ID: '{}'".format(membershipID), font = DEFAULT_FONT, bg = "#FFE45E")
        label4.grid(row = 5, column = 2, sticky = W)
        label5 = Label(win, text = "Member Name: '{}'".format(member_name), font = DEFAULT_FONT, bg = "#FFE45E")
        label5.grid(row = 6, column = 2, sticky = W)
        label6 = Label(win, text = "Due Date: '{}'".format(due_date), font = DEFAULT_FONT, bg = "#FFE45E")
        label6.grid(row = 7, column = 2, sticky = W)

        button1 = Button(win, text = "Confirm Loan", font = DEFAULT_FONT, bg = "#5AA9E6", command = loan_books)
        button1.grid(row = 8, column = 2)
        button2 = Button(win, text = "Back to Borrow Function", font = DEFAULT_FONT, bg = "#5AA9E6", command = win.destroy)
        button2.grid(row = 8, column = 3)
    else:
        label1 = Label(win, text = "Error!", font = TITLE_FONT)
        label1.pack()
        label2 = Label(win, text = "Book or member is invalid. Please enter the correct details.", font = DEFAULT_FONT)
        label2.pack() 
        btn = Button(win, text = "Back to Borrow Function", font = DEFAULT_FONT, bg = "#5AA9E6", command = win.destroy)
        btn.pack()
    
    win.mainloop()