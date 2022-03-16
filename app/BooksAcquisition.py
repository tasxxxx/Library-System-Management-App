import sqlalchemy as db
from tkinter import *

USERNAME = "root"
PASSWORD = "Hoepeng.0099"
HOST = "localhost"
PORT = 3306
DB = "Library"

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'
                          .format(USERNAME, PASSWORD, HOST, PORT, DB), echo=False)

cursor = engine.connect()

TITLE_FONT = ("Bahnschrift", 15)
DEFAULT_FONT = ("Bahnschrift", 11)

def booksAcquisition():
    
    root = Tk()
    root.configure(bg = "white")

    global accessionNo_field
    global title_field
    global authors_field
    global isbn_field 
    global publisher_field
    global publicationYear_field

    toplabel = Label(root, text = "For New Book Acquisition, Please Enter Required Information Below:", font = TITLE_FONT, bg = "#5AA9E6")
    toplabel.grid(row = 1, column = 2, columnspan = 2)

    label1 = Label(root, text = "Accession Number", font = DEFAULT_FONT, bg = "#FFE45E")
    label1.grid(row = 2, column = 2)
    label2 = Label(root, text = "Title", font = DEFAULT_FONT, bg = "#FFE45E")
    label2.grid(row = 3, column = 2)
    label3 = Label(root, text = "Authors", font = DEFAULT_FONT, bg = "#FFE45E")
    label3.grid(row = 4, column = 2)
    label4 = Label(root, text = "ISBN", font = DEFAULT_FONT, bg = "#FFE45E")
    label4.grid(row = 5, column = 2)
    label5 = Label(root, text = "Publisher", font = DEFAULT_FONT, bg = "#FFE45E")
    label5.grid(row = 6, column = 2)
    label6 = Label(root, text = "Publication Year", font = DEFAULT_FONT, bg = "#FFE45E")
    label6.grid(row = 7, column = 2)

    accessionNo_field = Entry(root, width = 30)
    accessionNo_field.grid(row = 2, column = 3, sticky = W)
    title_field = Entry(root, width = 30)
    title_field.grid(row = 3, column = 3, sticky = W)
    authors_field = Entry(root, width = 30)
    authors_field.grid(row = 4, column = 3, sticky = W)
    isbn_field = Entry(root, width = 30)
    isbn_field.grid(row = 5, column = 3, sticky = W)
    publisher_field = Entry(root, width = 30)
    publisher_field.grid(row = 6, column = 3, sticky = W)
    publicationYear_field = Entry(root, width = 30)
    publicationYear_field.grid(row = 7, column = 3, sticky = W)

    button1 = Button(root, text = "Add New Book", font = DEFAULT_FONT, bg = "#5AA9E6", command = popup_window)
    button1.grid(row = 8, column = 2)
    button2 = Button(root, text = "Back to Books Menu", font = DEFAULT_FONT, bg = "#5AA9E6", command = root.destroy)
    button2.grid(row = 8, column = 3)

    root.mainloop()

def popup_window():

    win = Tk()

    global accessionNo
    global title
    global authors
    global isbn 
    global publisher
    global publicationYear

    accessionNo = accessionNo_field.get()
    title = title_field.get()
    authors = authors_field.get()
    isbn = isbn_field.get()
    publisher = publisher_field.get()
    publicationYear = publicationYear_field.get()

    # Predicate: Whether book has been added
    sql1 = "SELECT * FROM Book WHERE accessionNo = '{}'".format(accessionNo)
    book_added = cursor.execute(sql1).fetchall()

    # Predicate: Whether entry has missing fields
    inputArr = [accessionNo, title, authors, isbn, publisher, publicationYear]
    
    if (len(book_added) > 0) or ("" in inputArr):
        label1 = Label(win, text = "Error!", font = TITLE_FONT)
        label1.pack()
        label2 = Label(win, text = "Book already added; Duplicate, Missing or Incomplete fields.", font = DEFAULT_FONT)
        label2.pack() 
        btn = Button(win, text = "Back to Acquisition Function", font = DEFAULT_FONT, bg = "#5AA9E6", command = win.destroy)
        btn.pack()
    else:
        # INSERT DATA INTO BOOK TABLE 
        add_book = "INSERT INTO Book (accessionNo, title, isbn, publisher, publicationYear) VALUES ('{}', '{}', '{}', '{}', '{}')".format(accessionNo, title, isbn, publisher, publicationYear)
        cursor.execute(add_book)

        # INSERT DATA INTO AUTHOR TABLE
        authorArr = authors.split(", ")
        for author in authorArr:
            add_author = "INSERT INTO Author (accessionNo, author) VALUES ('{}', '{}')".format(accessionNo, author)
            cursor.execute(add_author)

        label1 = Label(win, text = "Success!", font = TITLE_FONT)
        label1.pack()
        label2 = Label(win, text = "New Book added in Library.", font = DEFAULT_FONT)
        label2.pack() 
        btn = Button(win, text = "Back to Acquisition Function", font = DEFAULT_FONT, bg = "#5AA9E6", command = win.destroy)
        btn.pack()
    
    win.mainloop()