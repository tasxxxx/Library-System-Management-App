import sqlalchemy as db
from tkinter import *
from datetime import timedelta
from datetime import datetime

USERNAME = "root"
PASSWORD = "Crunchyapples99"
HOST = "localhost"
PORT = 3306
DB = "Library"

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
cursor = engine.connect()

TITLE_FONT = ("Bahnschrift", 15)
DEFAULT_FONT = ("Bahnschrift", 11)

def loansReturn():

    root = Tk()

    global accessionNo_field
    global returndate_field

    toplabel = Label(root, text = "To Return a Book, Please Enter Information Below:", font = TITLE_FONT, bg = "#5AA9E6")
    toplabel.grid(row = 1, column = 2, sticky = NSEW)

    label1 = Label(root, text = "Accession Number", font = DEFAULT_FONT, bg = "#FFE45E")
    label1.grid(row = 2, column = 2)
    label2 = Label(root, text = "Return Date", font = DEFAULT_FONT, bg = "#FFE45E")
    label2.grid(row = 3, column = 2)

    accessionNo_field = Entry(root, width = 30)
    accessionNo_field.grid(row = 2, column = 3, sticky = W)
    returndate_field = Entry(root, width = 30)
    returndate_field.grid(row = 3, column = 3, sticky = W)

    button1 = Button(root, text = "Return Book", font = DEFAULT_FONT, bg = "#5AA9E6", command = popup_window)
    button1.grid(row = 8, column = 2)
    button2 = Button(root, text = "Back to Loans Menu", font = DEFAULT_FONT, bg = "#5AA9E6", command = root.destroy)
    button2.grid(row = 8, column = 3)

    root.mainloop()

def return_books():

    win = Tk()

    # UPDATE BORROW TABLE'S RETURN DATE FIELD
    sql4 = "UPDATE Borrow SET returnDate = '{}' WHERE (accessionNo = '{}' AND borrowDate = '{}')".format(return_date, accessionNo, borrowdate)
    cursor.execute(sql4)

    win.mainloop()

def popup_window():

    win = Tk()

    global accessionNo
    global return_date
    global borrowdate
    accessionNo = accessionNo_field.get()
    return_date = returndate_field.get() # String

    # Predicate: Does Return Date > Due Date
    sql1 = "SELECT * FROM Borrow WHERE (accessionNo = '{}' AND returnDate IS null)".format(accessionNo)
    borrowdate = cursor.execute(sql1).fetchall()[0][1] # YYYY-MM-DD format in MySQL, returns date obj
    duedate = borrowdate + timedelta(days = 14) # Returns date obj
    a = datetime.strptime(return_date, '%Y/%m/%d').date() # Returns date obj
    fineAmount = 0
    if(a > duedate): # If return date exceeds due date, only update fine amount
        fineAmount = (a - duedate).days
    
    membershipID = cursor.execute(sql1).fetchall()[0][2]
    
    if (fineAmount > 0):
        # Error
        # UPDATE BORROW TABLE'S RETURN DATE FIELD AND FINE FOR MEMBER
        sql3 = "UPDATE Borrow SET returnDate = '{}' WHERE (accessionNo = '{}' AND borrowDate = '{}')".format(return_date, accessionNo, borrowdate)
        cursor.execute(sql3)
        aaa = "SELECT * FROM Fine WHERE memberId = '{}'".format(membershipID)
        existing_record = cursor.execute(aaa).fetchall()

        if (len(existing_record) > 0):
            old_amt = existing_record[0][1]
            new_amt = old_amt + fineAmount
            sql4 = "UPDATE Fine SET fineAmount = '{}' WHERE memberId = '{}'".format(new_amt, membershipID)
            cursor.execute(sql4)
        else:
            sql4 = "INSERT INTO Fine VALUES ('{}', '{}')".format(membershipID, fineAmount)
            cursor.execute(sql4)

        label1 = Label(win, text = "Error!", font = TITLE_FONT, bg = "#5AA9E6")
        label1.pack()
        label2 = Label(win, text = "Book returned successfully but has fines.", font = DEFAULT_FONT)
        label2.pack() 
        btn = Button(win, text = "Back to Return Function", font = DEFAULT_FONT, bg = "#5AA9E6", command = win.destroy)
        btn.pack()
    else:
        # Success
        # UPDATE BORROW TABLE'S RETURN DATE FIELD
        toplabel = Label(win, text = "Confirm Return Details To Be Correct", font = TITLE_FONT, bg = "#5AA9E6")
        toplabel.grid(row = 1, column = 2, sticky = NSEW)

        get_query = "SELECT * FROM Book WHERE accessionNo = '{}'".format(accessionNo)
        get_member = "SELECT * FROM Members WHERE memberId = '{}'".format(membershipID)
        book_title = cursor.execute(get_query).fetchall()[0][1]
        member_name = cursor.execute(get_member).fetchall()[0][1]

        label1 = Label(win, text = "Accession Number: '{}'".format(accessionNo), font = DEFAULT_FONT, bg = "#FFE45E")
        label1.grid(row = 2, column = 2, sticky = W)
        label2 = Label(win, text = "Book Title: '{}'".format(book_title), font = DEFAULT_FONT, bg = "#FFE45E")
        label2.grid(row = 3, column = 2, sticky = W)
        label3 = Label(win, text = "Membership ID: '{}'".format(membershipID), font = DEFAULT_FONT, bg = "#FFE45E")
        label3.grid(row = 4, column = 2, sticky = W)
        label4 = Label(win, text = "Member Name '{}'".format(member_name), font = DEFAULT_FONT, bg = "#FFE45E")
        label4.grid(row = 5, column = 2, sticky = W)
        label5 = Label(win, text = "Return Date: '{}'".format(return_date), font = DEFAULT_FONT, bg = "#FFE45E")
        label5.grid(row = 6, column = 2, sticky = W)
        label6 = Label(win, text = "Fine: $'{}'".format(fineAmount), font = DEFAULT_FONT, bg = "#FFE45E")
        label6.grid(row = 7, column = 2, sticky = W)

        button1 = Button(win, text = "Confirm Return", font = DEFAULT_FONT, bg = "#5AA9E6", command = return_books)
        button1.grid(row = 8, column = 2)
        button2 = Button(win, text = "Back to Return Function", font = DEFAULT_FONT, bg = "#5AA9E6", command = win.destroy)
        button2.grid(row = 8, column = 3)

    win.mainloop()