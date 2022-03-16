import sqlalchemy as db
from tkinter import *
from datetime import datetime
from datetime import timedelta
from datetime import date
import time

USERNAME = "root"
PASSWORD = "mysqlUbae!!1"
HOST = "localhost"
PORT = 3306
DB = "Library"

FONT = 'Arial'
FONT_SIZE = 25
SMALL_FONT_SIZE = 10
STYLE = 'bold'

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
cursor = engine.connect()

def loansBorrow():

    root = Tk()
    root.title("Borrow")
    root.geometry("1920x1080")
    root.configure(bg = "white")

    global accessionNo_field
    global membershipID_field

    toplabel = Label(root, text = "To Borrow a Book, Please Enter Information Below:", fg='black', bg='#c5e3e5', relief='raised', width=60, height=3)
    toplabel.config(font=(FONT, FONT_SIZE, STYLE))
    toplabel.place(relx=0.5, rely=0.09, anchor="center")

    label1 = Label(root, text = "Accession Number", bg = "#FFE45E")
    label1.config(font=(FONT, FONT_SIZE, STYLE))
    label1.place(relx=0.4, rely=0.4, anchor="center")
    label2 = Label(root, text = "Membership ID", bg = "#FFE45E")
    label2.config(font=(FONT, FONT_SIZE, STYLE))
    label2.place(relx=0.4, rely=0.6, anchor="center")

    accessionNo_field = Entry(root, width = 30)
    accessionNo_field.place(relx=0.6, rely=0.4, anchor="center")
    membershipID_field = Entry(root, width = 30)
    membershipID_field.place(relx=0.6, rely=0.6, anchor="center")

    button1 = Button(root, text = "Borrow Book", bg = "#5AA9E6", command = popup_window)
    button1.config(font=(FONT, FONT_SIZE, STYLE))
    button1.place(relx=0.4, rely=0.9, anchor="center")
    button2 = Button(root, text = "Back to Loans Menu", bg = "#5AA9E6", command = root.destroy)
    button2.config(font=(FONT, FONT_SIZE, STYLE))
    button2.place(relx=0.6, rely=0.9, anchor="center")

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
        win.geometry("800x400")
        win.configure(bg = "#eb1e1e")
        win.title("Error")
        label1 = Label(win, text = "Error!", bg = "#eb1e1e")
        label1.place(relx=0.5, rely=0.1, anchor="center")
        label1.config(font=(FONT, FONT_SIZE, STYLE))
        old_due_date = cursor.execute(sql1).fetchall()[0][1] + timedelta(days = 14)
        label2 = Label(win, text = "Book is currently on Loan until: '{}'".format(old_due_date.strftime("%d/%m/%Y")), bg = "#eb1e1e")
        label2.place(relx=0.5, rely=0.5, anchor="center")
        label2.config(font=(FONT, FONT_SIZE, STYLE))
        btn = Button(win, text = "Back to Borrow Function", bg = "#5AA9E6", command = win.destroy)
        btn.place(relx=0.5, rely=0.9, anchor="center")
        btn.config(font=(FONT, FONT_SIZE, STYLE))
    elif (len(on_reservation) > 0):
        # Error
        win.geometry("800x400")
        win.configure(bg = "#eb1e1e")
        win.title("Error")
        label1 = Label(win, text = "Error!", bg = "#eb1e1e")
        label1.place(relx=0.5, rely=0.1, anchor="center")
        label1.config(font=(FONT, FONT_SIZE, STYLE))
        label2 = Label(win, text = "Book is currently on Reservation", bg = "#eb1e1e")
        label2.place(relx=0.5, rely=0.5, anchor="center")
        label2.config(font=(FONT, FONT_SIZE, STYLE))
        btn = Button(win, text = "Back to Borrow Function", bg = "#5AA9E6", command = win.destroy)
        btn.place(relx=0.5, rely=0.9, anchor="center")
        btn.config(font=(FONT, FONT_SIZE, STYLE))
    elif (len(books_borrowed) == 2):
        # Error
        win.geometry("800x400")
        win.configure(bg = "#eb1e1e")
        win.title("Error")
        label1 = Label(win, text = "Error!", bg = "#eb1e1e")
        label1.place(relx=0.5, rely=0.1, anchor="center")
        label1.config(font=(FONT, FONT_SIZE, STYLE))
        label2 = Label(win, text = "Member loan quota exceeded.", bg = "#eb1e1e")
        label2.place(relx=0.5, rely=0.5, anchor="center")
        label2.config(font=(FONT, FONT_SIZE, STYLE))
        btn = Button(win, text = "Back to Borrow Function", bg = "#5AA9E6", command = win.destroy)
        btn.place(relx=0.5, rely=0.9, anchor="center")
        btn.config(font=(FONT, FONT_SIZE, STYLE))
    elif (fineamt > 0):
        # Error
        win.geometry("800x400")
        win.configure(bg = "#eb1e1e")
        win.title("Error")
        label1 = Label(win, text = "Error!", bg = "#eb1e1e")
        label1.place(relx=0.5, rely=0.1, anchor="center")
        label1.config(font=(FONT, FONT_SIZE, STYLE))
        label2 = Label(win, text = "Member has outstanding fine.", bg = "#eb1e1e")
        label2.place(relx=0.5, rely=0.5, anchor="center") 
        label2.config(font=(FONT, FONT_SIZE, STYLE))
        btn = Button(win, text = "Back to Borrow Function", bg = "#5AA9E6", command = win.destroy)
        btn.place(relx=0.5, rely=0.9, anchor="center")
        btn.config(font=(FONT, FONT_SIZE, STYLE))
    else:
        # Success
        win.geometry("800x400")
        win.configure(bg = "#b0f556")
        win.title("Success")
        label1 = Label(win, text = "Success!", bg = "#b0f556")
        label1.place(relx=0.5, rely=0.1, anchor="center")
        label1.config(font=(FONT, FONT_SIZE, STYLE))
        label2 = Label(win, text = "Book has been borrowed.", bg = "#b0f556")
        label2.place(relx=0.5, rely=0.5, anchor="center")
        label2.config(font=(FONT, FONT_SIZE, STYLE))
        btn = Button(win, text = "Back to Borrow Function", bg = "#5AA9E6", command = win.destroy)
        btn.place(relx=0.5, rely=0.9, anchor="center")
        btn.config(font=(FONT, FONT_SIZE, STYLE))

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
        win.geometry("400x800")
        win.configure(bg = "#b0f556")
        win.title("Confirmation")

        toplabel = Label(win, text = "Confirm Loan Details to Be Correct", bg = "#b0f556")
        toplabel.config(font=(FONT, FONT_SIZE, STYLE))
        toplabel.place(relx=0.5, rely=0.09, anchor="center")
        get_query = "SELECT * FROM Book WHERE accessionNo = '{}'".format(accessionNo)
        get_member = "SELECT * FROM Members WHERE memberId = '{}'".format(membershipID)
        book_title = cursor.execute(get_query).fetchall()[0][1]
        datetimeobj1 = date.today()
        borrow_date = datetimeobj1.strftime("%Y/%m/%d")
        member_name = cursor.execute(get_member).fetchall()[0][1]
        datetimeobj2 = datetimeobj1 + timedelta(days = 14)
        due_date = datetimeobj2.strftime("%Y/%m/%d")

        label1 = Label(win, text = "Accession Number: '{}'".format(accessionNo), bg = "#FFE45E")
        label1.config(font=(FONT, FONT_SIZE, STYLE))
        label1.place(relx=0.2, rely=0.2, anchor="w")
        label2 = Label(win, text = "Book Title: '{}'".format(book_title), bg = "#FFE45E")
        label2.config(font=(FONT, FONT_SIZE, STYLE))
        label2.place(relx=0.2, rely=0.3, anchor="w")
        label3 = Label(win, text = "Borrow Date: '{}'".format(borrow_date), bg = "#FFE45E")
        label3.config(font=(FONT, FONT_SIZE, STYLE))
        label3.place(relx=0.2, rely=0.4, anchor="w")
        label4 = Label(win, text = "Membership ID: '{}'".format(membershipID), bg = "#FFE45E")
        label4.config(font=(FONT, FONT_SIZE, STYLE))
        label4.place(relx=0.2, rely=0.5, anchor="w")
        label5 = Label(win, text = "Member Name: '{}'".format(member_name), bg = "#FFE45E")
        label5.config(font=(FONT, FONT_SIZE, STYLE))
        label5.place(relx=0.2, rely=0.6, anchor="w")
        label6 = Label(win, text = "Due Date: '{}'".format(due_date), bg = "#FFE45E")
        label6.config(font=(FONT, FONT_SIZE, STYLE))
        label6.place(relx=0.2, rely=0.7, anchor="w")

        button1 = Button(win, text = "Confirm Loan", bg = "#5AA9E6", command = loan_books)
        button1.config(font=(FONT, FONT_SIZE, STYLE))
        button1.place(relx=0.3, rely=0.9, anchor="center")
        button2 = Button(win, text = "Back to Borrow Function", bg = "#5AA9E6", command = win.destroy)
        button2.config(font=(FONT, FONT_SIZE, STYLE))
        button2.place(relx=0.6, rely=0.9, anchor="center")
    else:
        win.geometry("800x400")
        win.configure(bg = "#eb1e1e")
        win.title("Error")
        label1 = Label(win, text = "Error!", bg = "#eb1e1e")
        label1.place(relx=0.5, rely=0.1, anchor="center")
        label1.config(font=(FONT, FONT_SIZE, STYLE))
        label2 = Label(win, text = "Book or member is invalid. Please enter the correct details.", bg = "#eb1e1e", wraplength = 700)
        label2.place(relx=0.5, rely=0.5, anchor="center")
        label2.config(font=(FONT, FONT_SIZE, STYLE))
        btn = Button(win, text = "Back to Borrow Function", bg = "#5AA9E6", command = win.destroy)
        btn.place(relx=0.5, rely=0.9, anchor="center")
        btn.config(font=(FONT, FONT_SIZE, STYLE))
    
    win.mainloop()