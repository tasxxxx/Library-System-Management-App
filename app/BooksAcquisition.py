import sqlalchemy as db
from tkinter import *
from PIL import ImageTk, Image

USERNAME = "root"
PASSWORD = "Dcmmq9ck5s24!"
HOST = "localhost"
PORT = 3306
DB = "Library"

FONT = 'Arial'
FONT_SIZE = 25
SMALL_FONT_SIZE = 10
STYLE = 'bold'

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'
                          .format(USERNAME, PASSWORD, HOST, PORT, DB), echo=False)

cursor = engine.connect()

def booksAcquisition():
    
    root = Toplevel()
    root.title("Book Acquisition")
    root.geometry("1920x1080")
    root.configure(bg = "white")

    image = Image.open("bg1.jpg")
    image = image.resize((1300, 650))

    bg = ImageTk.PhotoImage(image)
    canvas1 = Canvas(root, width = 1920, height = 1080)
    canvas1.pack(fill = "both", expand =  True)
    canvas1.create_image(0, 0, image = bg, anchor = "nw")

    global accessionNo_field
    global title_field
    global authors_field
    global isbn_field 
    global publisher_field
    global publicationYear_field

    toplabel = Label(root, text = "For New Book Acquisition, Please Enter Required Information Below:", fg='black', bg='#c5e3e5', relief='raised', width=60, height=3)
    toplabel.config(font=(FONT, FONT_SIZE, STYLE))
    toplabel.place(relx=0.5, rely=0.09, anchor="center")

    label1 = Label(root, text = "Accession Number", bg = "#FFE45E")
    label1.config(font=(FONT, FONT_SIZE, STYLE))
    label1.place(relx=0.2, rely=0.2, anchor="center")
    label2 = Label(root, text = "Title", bg = "#FFE45E")
    label2.config(font=(FONT, FONT_SIZE, STYLE))
    label2.place(relx=0.2, rely=0.3, anchor="center")
    label3 = Label(root, text = "Authors", bg = "#FFE45E")
    label3.config(font=(FONT, FONT_SIZE, STYLE))
    label3.place(relx=0.2, rely=0.4, anchor="center")
    label4 = Label(root, text = "ISBN", bg = "#FFE45E")
    label4.config(font=(FONT, FONT_SIZE, STYLE))
    label4.place(relx=0.2, rely=0.5, anchor="center")
    label5 = Label(root, text = "Publisher", bg = "#FFE45E")
    label5.config(font=(FONT, FONT_SIZE, STYLE))
    label5.place(relx=0.2, rely=0.6, anchor="center")
    label6 = Label(root, text = "Publication Year", bg = "#FFE45E")
    label6.config(font=(FONT, FONT_SIZE, STYLE))
    label6.place(relx=0.2, rely=0.7, anchor="center")

    accessionNo_field = Entry(root, width = 30)
    accessionNo_field.place(relx=0.65, rely=0.2, width = 660, height = 40, anchor="center")
    title_field = Entry(root, width = 30)
    title_field.place(relx=0.65, rely=0.3, width = 660, height = 40, anchor="center")
    authors_field = Entry(root, width = 30)
    authors_field.place(relx=0.65, rely=0.4, width = 660, height = 40, anchor="center")
    isbn_field = Entry(root, width = 30)
    isbn_field.place(relx=0.65, rely=0.5, width = 660, height = 40, anchor="center")
    publisher_field = Entry(root, width = 30)
    publisher_field.place(relx=0.65, rely=0.6, width = 660, height = 40, anchor="center")
    publicationYear_field = Entry(root, width = 30)
    publicationYear_field.place(relx=0.65, rely=0.7, width = 660, height = 40, anchor="center")

    button1 = Button(root, text = "Add New Book", bg = "#5AA9E6", command = popup_window)
    button1.config(font=(FONT, FONT_SIZE, STYLE))
    button1.place(relx=0.3, rely=0.9, anchor="center")
    button2 = Button(root, text = "Back to Books Menu", bg = "#5AA9E6", command = root.destroy)
    button2.config(font=(FONT, FONT_SIZE, STYLE))
    button2.place(relx=0.6, rely=0.9, anchor="center")

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
        win.geometry("800x400")
        win.configure(bg = "#eb1e1e")
        label1 = Label(win, text = "Error!", bg = "#eb1e1e")
        label1.place(relx=0.5, rely=0.1, anchor="center")
        label1.config(font=(FONT, FONT_SIZE, STYLE))
        label2 = Label(win, text = "Book already added; Duplicate, Missing or Incomplete fields.", bg = "#eb1e1e", wraplength = 700)
        label2.place(relx=0.5, rely=0.5, anchor="center")
        label2.config(font=(FONT, FONT_SIZE, STYLE))
        btn = Button(win, text = "Back to Acquisition Function", bg = "#5AA9E6", command = win.destroy)
        btn.place(relx=0.5, rely=0.9, anchor="center")
        btn.config(font=(FONT, FONT_SIZE, STYLE))
    else:
        # INSERT DATA INTO BOOK TABLE 
        add_book = "INSERT INTO Book (accessionNo, title, isbn, publisher, publicationYear) VALUES ('{}', '{}', '{}', '{}', '{}')".format(accessionNo, title, isbn, publisher, publicationYear)
        cursor.execute(add_book)

        # INSERT DATA INTO AUTHOR TABLE
        authorArr = authors.split(", ")
        for author in authorArr:
            add_author = "INSERT INTO Author (accessionNo, author) VALUES ('{}', '{}')".format(accessionNo, author)
            cursor.execute(add_author)

        win.geometry("800x400")
        win.configure(bg = "#b0f556")
        label1 = Label(win, text = "Success!", bg = "#b0f556")
        label1.place(relx=0.5, rely=0.1, anchor="center")
        label1.config(font=(FONT, FONT_SIZE, STYLE))
        label2 = Label(win, text = "New Book added in Library.", bg = "#b0f556", wraplength = 700)
        label2.place(relx=0.5, rely=0.5, anchor="center")
        label2.config(font=(FONT, FONT_SIZE, STYLE))
        btn = Button(win, text = "Back to Acquisition Function", bg = "#5AA9E6", command = win.destroy)
        btn.place(relx=0.5, rely=0.9, anchor="center")
        btn.config(font=(FONT, FONT_SIZE, STYLE))
    
    win.mainloop()