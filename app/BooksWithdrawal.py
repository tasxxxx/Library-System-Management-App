import sqlalchemy as db
from tkinter import *

USERNAME = "root"
PASSWORD = "m"
HOST = "localhost"
PORT = 3306
DB = "Library"

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
cursor = engine.connect()

TITLE_FONT = ("Bahnschrift", 15)
DEFAULT_FONT = ("Bahnschrift", 11)

def booksWithdrawal():

    root = Tk()

    global accessionNo_field

    toplabel = Label(root, text = "To Remove Outdated Books From System, Please Enter Required Information Below:", font = TITLE_FONT)
    toplabel.grid(row = 1, column = 2, sticky = NSEW)

    label = Label(root, text = "Accession Number", font = DEFAULT_FONT, bg = "#FFE45E")
    label.grid(row = 2, column = 2)

    accessionNo_field = Entry(root, width = 30)
    accessionNo_field.grid(row = 2, column = 3, sticky = W)

    button1 = Button(root, text = "Withdraw Book", font = DEFAULT_FONT, bg = "#5AA9E6", command = popup_window)
    button1.grid(row = 8, column = 2)
    button2 = Button(root, text = "Back to Books Menu", font = DEFAULT_FONT, bg = "#5AA9E6", command = root.destroy)
    button2.grid(row = 8, column = 3)

    root.mainloop()

def withdraw_books():

    win = Tk()

    # Predicate: Whether book is on loan / on reservation / not in database
    sql1 = "SELECT * FROM Borrow WHERE accessionNo = {}".format(accessionNo)
    on_loan = cursor.execute(sql1).fetchall()
    sql2 = "SELECT * FROM Reservation WHERE accessionNo = {}".format(accessionNo)
    on_reservation = cursor.execute(sql2).fetchall()
    sql3 = "SELECT * FROM Book WHERE accessionNo = {}".format(accessionNo)
    in_database = cursor.execute(sql3).fetchall()

    if (len(on_loan) > 0):
        # Error
        label1 = Label(win, text = "Error!", font = TITLE_FONT)
        label1.pack()
        label2 = Label(win, text = "Book is currently on Loan.", font = DEFAULT_FONT)
        label2.pack() 
        btn = Button(win, text = "Return to Withdrawal Function", font = DEFAULT_FONT, bg = "#5AA9E6", command = win.destroy)
        btn.pack()
    elif (len(on_reservation) > 0):
        # Error
        label1 = Label(win, text = "Error!", font = TITLE_FONT)
        label1.pack()
        label2 = Label(win, text = "Book is currently Reserved.", font = DEFAULT_FONT)
        label2.pack() 
        btn = Button(win, text = "Return to Withdrawal Function", font = DEFAULT_FONT, bg = "#5AA9E6", command = win.destroy)
        btn.pack()
    elif (len(in_database) < 1):
        # Error
        label1 = Label(win, text = "Error!", font = TITLE_FONT)
        label1.pack()
        label2 = Label(win, text = "Book is not in Database.", font = DEFAULT_FONT)
        label2.pack() 
        btn = Button(win, text = "Return to Withdrawal Function", font = DEFAULT_FONT, bg = "#5AA9E6", command = win.destroy)
        btn.pack()
    else:
        # Success
        label1 = Label(win, text = "Success!", font = TITLE_FONT)
        label1.pack()
        label2 = Label(win, text = "Book has been removed.", font = DEFAULT_FONT)
        label2.pack() 
        btn = Button(win, text = "Return to Withdrawal Function", font = DEFAULT_FONT, bg = "#5AA9E6", command = win.destroy)
        btn.pack()

        # DELETE DATA FROM AUTHOR
        sql3 = "DELETE FROM Author WHERE accessionNo = {}".format(accessionNo)
        cursor.execute(sql3)

        # DELETE DATA FROM BOOK
        sql4 = "DELETE FROM Book WHERE accessionNo = {}".format(accessionNo)
        cursor.execute(sql4)

    win.mainloop()

def popup_window():

    win = Tk()

    global accessionNo
    accessionNo = accessionNo_field.get()

    # Green confirmation window
    toplabel = Label(win, text = "Please Confirm Details to Be Correct", font = TITLE_FONT)
    toplabel.grid(row = 1, column = 2, sticky = NSEW)
    get_query = "SELECT * FROM Book WHERE accessionNo = {}".format(accessionNo)
    get_author = "SELECT * FROM Author WHERE accessionNo = {}".format(accessionNo)
    book_title = cursor.execute(get_query).fetchall()[0][1]
    author = cursor.execute(get_author).fetchall()
    isbn = cursor.execute(get_query).fetchall()[0][2]
    publisher = cursor.execute(get_query).fetchall()[0][3]
    year = cursor.execute(get_query).fetchall()[0][4]

    authors = []
    for i in range(len(author)):
        authors = authors.append(cursor.execute(get_author).fetchall()[i][1])
        
    label1 = Label(win, text = "Accession Number: {}".format(accessionNo), font = DEFAULT_FONT, bg = "#FFE45E")
    label1.grid(row = 2, column = 2, sticky = W)
    label2 = Label(win, text = "Title: {}".format(book_title), font = DEFAULT_FONT, bg = "#FFE45E")
    label2.grid(row = 3, column = 2, sticky = W)
    label3 = Label(win, text = "Authors: {}".format(', '.join(authors)), font = DEFAULT_FONT, bg = "#FFE45E")
    label3.grid(row = 4, column = 2, sticky = W)
    label4 = Label(win, text = "ISBN: {}".format(isbn), font = DEFAULT_FONT, bg = "#FFE45E")
    label4.grid(row = 5, column = 2, sticky = W)
    label5 = Label(win, text = "Publisher: {}".format(publisher), font = DEFAULT_FONT, bg = "#FFE45E")
    label5.grid(row = 6, column = 2, sticky = W)
    label6 = Label(win, text = "Year: {}".format(year), font = DEFAULT_FONT, bg = "#FFE45E")
    label6.grid(row = 7, column = 2, sticky = W)

    button1 = Button(win, text = "Confirm Withdrawal", font = DEFAULT_FONT, bg = "#5AA9E6", command = lambda: [withdraw_books(), win.destroy()])
    button1.grid(row = 8, column = 2)
    button2 = Button(win, text = "Back to Withdrawal Function", font = DEFAULT_FONT, bg = "#5AA9E6", command = win.destroy)
    button2.grid(row = 8, column = 3)

    win.mainloop()