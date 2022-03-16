import sqlalchemy as db
from tkinter import *
from datetime import timedelta
from datetime import datetime

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

def loansReturn():

    root = Tk()
    root.title("Return")
    root.geometry("1920x1080")
    root.configure(bg = "white")

    global accessionNo_field
    global returndate_field

    toplabel = Label(root, text = "To Return a Book, Please Enter Information Below:", fg='black', bg='#c5e3e5', relief='raised', width=60, height=3)
    toplabel.config(font=(FONT, FONT_SIZE, STYLE))
    toplabel.place(relx=0.5, rely=0.09, anchor="center")

    label1 = Label(root, text = "Accession Number", bg = "#FFE45E")
    label1.config(font=(FONT, FONT_SIZE, STYLE))
    label1.place(relx=0.4, rely=0.4, anchor="center")
    label2 = Label(root, text = "Return Date", bg = "#FFE45E")
    label2.config(font=(FONT, FONT_SIZE, STYLE))
    label2.place(relx=0.4, rely=0.6, anchor="center")

    accessionNo_field = Entry(root, width = 30)
    accessionNo_field.place(relx=0.6, rely=0.4, anchor="center")
    returndate_field = Entry(root, width = 30)
    returndate_field.place(relx=0.6, rely=0.6, anchor="center")

    button1 = Button(root, text = "Return Book", bg = "#5AA9E6", command = popup_window)
    button1.config(font=(FONT, FONT_SIZE, STYLE))
    button1.place(relx=0.4, rely=0.9, anchor="center")
    button2 = Button(root, text = "Back to Loans Menu", bg = "#5AA9E6", command = root.destroy)
    button2.config(font=(FONT, FONT_SIZE, STYLE))
    button2.place(relx=0.6, rely=0.9, anchor="center")

    root.mainloop()

def return_books():

    win = Tk()

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

        win.geometry("800x400")
        win.configure(bg = "#eb1e1e")
        win.title("Error")
        label1 = Label(win, text = "Error!", bg = "#eb1e1e")
        label1.place(relx=0.5, rely=0.1, anchor="center")
        label1.config(font=(FONT, FONT_SIZE, STYLE))
        label2 = Label(win, text = "Book returned successfully but has fines.", bg = "#eb1e1e")
        label2.place(relx=0.5, rely=0.5, anchor="center")
        label2.config(font=(FONT, FONT_SIZE, STYLE))
        btn = Button(win, text = "Back to Return Function", bg = "#5AA9E6", command = win.destroy)
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
        label2 = Label(win, text = "Book returned successfully.", bg = "#b0f556")
        label2.place(relx=0.5, rely=0.5, anchor="center")
        label2.config(font=(FONT, FONT_SIZE, STYLE))
        btn = Button(win, text = "Back to Return Function", bg = "#5AA9E6", command = win.destroy)
        btn.place(relx=0.5, rely=0.9, anchor="center")
        btn.config(font=(FONT, FONT_SIZE, STYLE))

        # UPDATE BORROW TABLE'S RETURN DATE FIELD
        sql4 = "UPDATE Borrow SET returnDate = '{}' WHERE (accessionNo = '{}' AND borrowDate = '{}')".format(return_date, accessionNo, borrowdate)
        cursor.execute(sql4)

    win.mainloop()

def popup_window():

    win = Tk()

    global accessionNo
    global return_date
    global borrowdate
    global membershipID
    global fineAmount
    accessionNo = accessionNo_field.get()
    return_date = returndate_field.get() # String

    # Predicate: Whether book is in database
    sql01 = "SELECT * FROM Borrow WHERE accessionNo = '{}' AND returnDate IS null".format(accessionNo)
    book_valid = cursor.execute(sql01).fetchall()

    if (len(book_valid) > 0):
        win.geometry("400x800")
        win.configure(bg = "#b0f556")
        win.title("Confirmation")

        # Predicate: Does Return Date > Due Date
        sql1 = "SELECT * FROM Borrow WHERE (accessionNo = '{}' AND returnDate IS null)".format(accessionNo)
        membershipID = cursor.execute(sql1).fetchall()[0][2]
        borrowdate = cursor.execute(sql1).fetchall()[0][1] # YYYY-MM-DD format in MySQL, returns date obj
        duedate = borrowdate + timedelta(days = 14) # Returns date obj
        a = datetime.strptime(return_date, '%Y/%m/%d').date() # Returns date obj    

        fineAmount = 0
        if(a > duedate): # If return date exceeds due date, only update fine amount
            fineAmount = (a - duedate).days

        toplabel = Label(win, text = "Confirm Return Details To Be Correct", bg = "#b0f556")
        toplabel.config(font=(FONT, FONT_SIZE, STYLE))
        toplabel.place(relx=0.5, rely=0.09, anchor="center")

        get_query = "SELECT * FROM Book WHERE accessionNo = '{}'".format(accessionNo)
        get_member = "SELECT * FROM Members WHERE memberId = '{}'".format(membershipID)
        book_title = cursor.execute(get_query).fetchall()[0][1]
        member_name = cursor.execute(get_member).fetchall()[0][1]

        label1 = Label(win, text = "Accession Number: '{}'".format(accessionNo), bg = "#FFE45E")
        label1.config(font=(FONT, FONT_SIZE, STYLE))
        label1.place(relx=0.2, rely=0.2, anchor="w")
        label2 = Label(win, text = "Book Title: '{}'".format(book_title), bg = "#FFE45E")
        label2.config(font=(FONT, FONT_SIZE, STYLE))
        label2.place(relx=0.2, rely=0.3, anchor="w")
        label3 = Label(win, text = "Membership ID: '{}'".format(membershipID), bg = "#FFE45E")
        label3.config(font=(FONT, FONT_SIZE, STYLE))
        label3.place(relx=0.2, rely=0.4, anchor="w")
        label4 = Label(win, text = "Member Name '{}'".format(member_name), bg = "#FFE45E")
        label4.config(font=(FONT, FONT_SIZE, STYLE))
        label4.place(relx=0.2, rely=0.5, anchor="w")
        label5 = Label(win, text = "Return Date: '{}'".format(return_date), bg = "#FFE45E")
        label5.config(font=(FONT, FONT_SIZE, STYLE))
        label5.place(relx=0.2, rely=0.6, anchor="w")
        label6 = Label(win, text = "Fine: $'{}'".format(fineAmount), bg = "#FFE45E")
        label6.config(font=(FONT, FONT_SIZE, STYLE))
        label6.place(relx=0.2, rely=0.7, anchor="w")

        button1 = Button(win, text = "Confirm Return", bg = "#5AA9E6", command = return_books)
        button1.config(font=(FONT, FONT_SIZE, STYLE))
        button1.place(relx=0.3, rely=0.9, anchor="center")
        button2 = Button(win, text = "Back to Return Function", bg = "#5AA9E6", command = win.destroy)
        button2.config(font=(FONT, FONT_SIZE, STYLE))
        button2.place(relx=0.6, rely=0.9, anchor="center")
    else:
        win.geometry("800x400")
        win.configure(bg = "#eb1e1e")
        win.title("Error")
        label1 = Label(win, text = "Error!", bg = "#eb1e1e")
        label1.place(relx=0.5, rely=0.1, anchor="center")
        label1.config(font=(FONT, FONT_SIZE, STYLE))
        label2 = Label(win, text = "Book is invalid. Book has been returned or there is no such book. Please enter the correct details.", bg = "#eb1e1e", wraplength = 700)
        label2.place(relx=0.5, rely=0.5, anchor="center")
        label2.config(font=(FONT, FONT_SIZE, STYLE))
        btn = Button(win, text = "Back to Return Function", bg = "#5AA9E6", command = win.destroy)
        btn.place(relx=0.5, rely=0.9, anchor="center")
        btn.config(font=(FONT, FONT_SIZE, STYLE))

    win.mainloop()