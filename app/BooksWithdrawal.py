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

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
cursor = engine.connect()

def booksWithdrawal():

    root = Toplevel()
    root.title("Book Withdrawal")
    root.geometry("1920x1080")
    root.configure(bg = "white")

    image = Image.open("bg1.jpg")
    image = image.resize((1300, 650))

    bg = ImageTk.PhotoImage(image)
    canvas1 = Canvas(root, width = 1920, height = 1080)
    canvas1.pack(fill = "both", expand =  True)
    canvas1.create_image(0, 0, image = bg, anchor = "nw")

    global accessionNo_field

    toplabel = Label(root, text = "To Remove Outdated Books From System, Please Enter Required Information Below:")
    toplabel.config(font=(FONT, FONT_SIZE, STYLE))
    toplabel.place(relx=0.5, rely=0.09, anchor="center")

    label = Label(root, text = "Accession Number", bg = "#FFE45E")
    label.config(font=(FONT, FONT_SIZE, STYLE))
    label.place(relx=0.2, rely=0.2, anchor="center")

    accessionNo_field = Entry(root, width = 30)
    accessionNo_field.place(relx=0.65, rely=0.2, width = 660, height = 40, anchor="center")

    button1 = Button(root, text = "Withdraw Book", bg = "#5AA9E6", command = popup_window)
    button1.config(font=(FONT, FONT_SIZE, STYLE))
    button1.place(relx=0.3, rely=0.9, anchor="center")
    button2 = Button(root, text = "Back to Books Menu", bg = "#5AA9E6", command = root.destroy)
    button2.config(font=(FONT, FONT_SIZE, STYLE))
    button2.place(relx=0.6, rely=0.9, anchor="center")

    root.mainloop()

def withdraw_books():

    win = Tk()

    # Predicate: Whether book is on loan / on reservation
    sql1 = "SELECT * FROM Borrow WHERE accessionNo = '{}' AND returnDate IS NULL".format(accessionNo)
    on_loan = cursor.execute(sql1).fetchall()
    sql2 = "SELECT * FROM Reservation WHERE accessionNo = '{}'".format(accessionNo)
    on_reservation = cursor.execute(sql2).fetchall()

    if (len(on_loan) > 0):
        # Error
        win.geometry("400x400")
        win.configure(bg = "#eb1e1e")
        label1 = Label(win, text = "Error!", bg = "#eb1e1e")
        label1.place(relx=0.5, rely=0.1, anchor="center")
        label1.config(font=(FONT, FONT_SIZE, STYLE))
        label2 = Label(win, text = "Book is currently on Loan.", bg = "#eb1e1e")
        label2.place(relx=0.5, rely=0.5, anchor="center")
        label2.config(font=(FONT, FONT_SIZE, STYLE))
        btn = Button(win, text = "Return to Withdrawal Function", bg = "#5AA9E6", command = win.destroy)
        btn.place(relx=0.5, rely=0.9, anchor="center")
        btn.config(font=(FONT, FONT_SIZE, STYLE))
    elif (len(on_reservation) > 0):
        # Error
        win.geometry("400x400")
        win.configure(bg = "#eb1e1e")
        label1 = Label(win, text = "Error!", bg = "#eb1e1e")
        label1.place(relx=0.5, rely=0.1, anchor="center")
        label1.config(font=(FONT, FONT_SIZE, STYLE))
        label2 = Label(win, text = "Book is currently Reserved.", bg = "#eb1e1e")
        label2.place(relx=0.5, rely=0.5, anchor="center")
        label2.config(font=(FONT, FONT_SIZE, STYLE))
        btn = Button(win, text = "Return to Withdrawal Function", bg = "#5AA9E6", command = win.destroy)
        btn.place(relx=0.5, rely=0.9, anchor="center")
        btn.config(font=(FONT, FONT_SIZE, STYLE))
    else:
        # Success
        win.geometry("400x400")
        win.configure(bg = "#b0f556")
        label1 = Label(win, text = "Success!", bg = "#b0f556")
        label1.place(relx=0.5, rely=0.1, anchor="center")
        label1.config(font=(FONT, FONT_SIZE, STYLE))
        label2 = Label(win, text = "Book has been removed.", bg = "#b0f556")
        label2.place(relx=0.5, rely=0.5, anchor="center")
        label2.config(font=(FONT, FONT_SIZE, STYLE))
        btn = Button(win, text = "Return to Withdrawal Function", bg = "#5AA9E6", command = win.destroy)
        btn.place(relx=0.5, rely=0.9, anchor="center")
        btn.config(font=(FONT, FONT_SIZE, STYLE))

        # DELETE DATA FROM AUTHOR
        sql3 = "DELETE FROM Author WHERE accessionNo = '{}'".format(accessionNo)
        cursor.execute(sql3)

        # DELETE DATA FROM BOOK
        sql4 = "DELETE FROM Book WHERE accessionNo = '{}'".format(accessionNo)
        cursor.execute(sql4)

    win.mainloop()

def popup_window():

    win1 = Tk()

    global accessionNo
    accessionNo = accessionNo_field.get()

    # Whether book is in database
    sql3 = "SELECT * FROM Book WHERE accessionNo = '{}'".format(accessionNo)
    in_database = cursor.execute(sql3).fetchall()

    if (len(in_database) < 1):
        # Error
        win1.geometry("400x400")
        win1.configure(bg = "#eb1e1e")
        label1 = Label(win1, text = "Error!", bg = "#eb1e1e")
        label1.place(relx=0.5, rely=0.1, anchor="center")
        label1.config(font=(FONT, FONT_SIZE, STYLE))
        label2 = Label(win1, text = "Book is not in Database.", bg = "#eb1e1e")
        label2.place(relx=0.5, rely=0.5, anchor="center")
        label2.config(font=(FONT, FONT_SIZE, STYLE))
        btn = Button(win1, text = "Return to Withdrawal Function", bg = "#5AA9E6", command = win1.destroy)
        btn.place(relx=0.5, rely=0.9, anchor="center")
        btn.config(font=(FONT, FONT_SIZE, STYLE))
    else:
        # Green confirmation window
        win1.geometry("400x800")
        win1.configure(bg = "#b0f556")
        toplabel = Label(win1, text = "Please Confirm Details to Be Correct", bg = "#b0f556")
        toplabel.config(font=(FONT, FONT_SIZE, STYLE))
        toplabel.place(relx=0.5, rely=0.09, anchor="center")
        get_query = "SELECT * FROM Book WHERE accessionNo = '{}'".format(accessionNo)
        get_author = "SELECT * FROM Author WHERE accessionNo = '{}'".format(accessionNo)
        book_title = cursor.execute(get_query).fetchall()[0][1]
        author = cursor.execute(get_author).fetchall()
        isbn = cursor.execute(get_query).fetchall()[0][2]
        publisher = cursor.execute(get_query).fetchall()[0][3]
        year = cursor.execute(get_query).fetchall()[0][4]

        authors = []
        for i in range(len(author)):
            authors.append(cursor.execute(get_author).fetchall()[i][1])
            
        label1 = Label(win1, text = "Accession Number: '{}'".format(accessionNo), bg = "#FFE45E")
        label1.config(font=(FONT, FONT_SIZE, STYLE))
        label1.place(relx=0.4, rely=0.2, anchor="w")
        label2 = Label(win1, text = "Title: '{}'".format(book_title), bg = "#FFE45E")
        label2.config(font=(FONT, FONT_SIZE, STYLE))
        label2.place(relx=0.4, rely=0.3, anchor="w")
        label3 = Label(win1, text = "Authors: '{}'".format(', '.join(authors)), bg = "#FFE45E")
        label3.config(font=(FONT, FONT_SIZE, STYLE))
        label3.place(relx=0.4, rely=0.4, anchor="w")
        label4 = Label(win1, text = "ISBN: '{}'".format(isbn), bg = "#FFE45E")
        label4.config(font=(FONT, FONT_SIZE, STYLE))
        label4.place(relx=0.4, rely=0.5, anchor="w")
        label5 = Label(win1, text = "Publisher: '{}'".format(publisher), bg = "#FFE45E")
        label5.config(font=(FONT, FONT_SIZE, STYLE))
        label5.place(relx=0.4, rely=0.6, anchor="w")
        label6 = Label(win1, text = "Year: '{}'".format(year), bg = "#FFE45E")
        label6.config(font=(FONT, FONT_SIZE, STYLE))
        label6.place(relx=0.4, rely=0.7, anchor="w")

        button1 = Button(win1, text = "Confirm Withdrawal", bg = "#5AA9E6", command = lambda: [withdraw_books(), win1.destroy()])
        button1.config(font=(FONT, FONT_SIZE, STYLE))
        button1.place(relx=0.3, rely=0.9, anchor="center")
        button2 = Button(win1, text = "Back to Withdrawal Function", bg = "#5AA9E6", command = win1.destroy)
        button2.config(font=(FONT, FONT_SIZE, STYLE))
        button2.place(relx=0.6, rely=0.9, anchor="center")

    win1.mainloop()