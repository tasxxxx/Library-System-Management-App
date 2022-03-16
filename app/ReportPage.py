import sqlalchemy as db
import tkinter as tk
import pandas as pd
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import showinfo

FONT = 'Arial'
FONT_SIZE = 25
SMALL_FONT_SIZE = 10
STYLE = 'bold'

# Create a database or connect to one
USERNAME = "root"
PASSWORD = "Hoepeng.0099"
HOST = "localhost"
PORT = 3306
DB = "Library"


# 11 FUNCTION FOR BOOK SEACRH
def book_search():
    engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'
                              .format(USERNAME, PASSWORD, HOST, PORT, DB), echo=False)

    # Create Cursor
    cursor = engine.connect()

    # Change to a Top Level rather than a new instance
    root = tk.Toplevel()
    root.title('Book Search Results')
    root.geometry('1225x225')

    columns = ('accessionNo', 'title', 'authors', 'isbn', 'publisher', 'publicationYear')

    tree = ttk.Treeview(root, columns=columns, show='headings')

    tree.heading('accessionNo', text='Accession Number')
    tree.heading('title', text='Title')
    tree.heading('authors', text='Authors')
    tree.heading('isbn', text='ISBN')
    tree.heading('publisher', text='Publisher')
    tree.heading('publicationYear', text='Publication Year')

    # Query the Database
    # 1. Check that only one word has been used for the search fields/attributes
    t = title_entry.get()
    a = authors_entry.get()
    i = isbn_entry.get()
    p = publisher_entry.get()
    py = publisher_year_entry.get()

    book_entries = [t, i, p, py]
    fields = ['title', 'isbn', 'publisher', 'publicationYear']
    book_query = {}

    for entry, field in zip(book_entries, fields):
        if entry == "":
            continue
        else:
            book_query[field] = entry

    if (len(t.split()) > 1 or len(a.split()) > 1 or len(i.split()) > 1 or len(p.split()) > 1 or len(py.split()) > 1):
        root.title("ERROR")
        root.geometry("800x400")
        root.configure(bg="#eb1e1e")

        error_label = tk.Label(root, text="ERROR: You may only enter one word per search field. Please try again.", bg="#eb1e1e", wraplength = 700)
        error_label.config(font=(FONT, FONT_SIZE, STYLE))
        error_label.place(relx=0.5, rely=0.1, anchor="center")
        # back to main page button
        btn = tk.Button(root, text="Back to Reports Menu", command=root.destroy)
        btn.config(font=(FONT, FONT_SIZE, STYLE))
        btn.place(relx=0.5, rely=0.9, anchor="center")
    else:
        statement = '''SELECT b.accessionNo, b.title, a.author, b.isbn, b.publisher, b.publicationYear 
                    FROM Book b 
                    JOIN Author a ON b.accessionNo = a.accessionNo'''

        add_on_condition = ""
        CLAUSE = ["WHERE", "AND"]
        rotation = 0

        # If there is a field entry for author:
        if len(a) > 0:
            author_condition = " WHERE a.accessionNo IN (SELECT accessionNo FROM Author WHERE author REGEXP '(^|[[:space:]]){}([[:space:]]|$)')".format(
                a)
            add_on_condition += author_condition
            rotation += 1

        if len(book_query) > 0:
            for field, val in book_query.items():
                if field == 'isbn' or field == 'publicationYear':
                    book_cond = " {} {} = '{}' ".format(CLAUSE[rotation], field, val)
                else:
                    book_cond = " {} {} REGEXP '(^|[[:space:]]){}([[:space:]]|$)' ".format(CLAUSE[rotation], field, val)
                if rotation == 0:
                    rotation += 1
                add_on_condition += book_cond

        statement += add_on_condition

        all_books_result = cursor.execute(statement).fetchall()

    search_results = []
    for n in range(len(all_books_result)):
        search_results.append((all_books_result[n][0], all_books_result[n][1], all_books_result[n][2],
                               all_books_result[n][3], all_books_result[n][4], all_books_result[n][5]))

    for search in search_results:
        tree.insert('', tk.END, values=search)

    def item_selected(event):
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']
            # show a message
            showinfo(title='Information', message=','.join(record))

    tree.bind('<<TreeviewSelect>>', item_selected)

    tree.grid(row=0, column=0, sticky='nsew')

    # add a scrollbar
    scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    # back to main page button
    btn = tk.Button(root, text="Back to Reports Menu", command=root.destroy).grid(row=1, column=0)

    root.mainloop()


# 15 FUNCTION TO SHOW BOOKS ON LOAN PER MEMBER
def mem_books():
    engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'
                              .format(USERNAME, PASSWORD, HOST, PORT, DB), echo=False)

    # Create Cursor
    cursor = engine.connect()

    root = tk.Toplevel()
    root.title('Books on Loan to Member')
    root.geometry('1250x225')

    columns = ('accessionNo', 'title', 'authors', 'isbn', 'publisher', 'publisherYear')

    tree = ttk.Treeview(root, columns=columns, show='headings')

    tree.heading('accessionNo', text='Accession Number')
    tree.heading('title', text='Title')
    tree.heading('authors', text='Authors')
    tree.heading('isbn', text='ISBN')
    tree.heading('publisher', text='Publisher')
    tree.heading('publisherYear', text='Publisher Year')

    # Query the Database
    ## MEMBERSHIP_ID EXISTS HENCE CONDUCT QUERY 
    # 1. does membership id exist
    id_exists = '''SELECT EXISTS(SELECT * FROM Members WHERE memberId = '{0}')'''.format(memberId_entry.get())
    result = cursor.execute(id_exists).fetchall()

    if result[0][0] == 1:
        # 2. membership id exists, check for whether books are on loan
        members = '''SELECT EXISTS(
                    SELECT b.accessionNo, b.title, a.author, b.isbn, b.publisher, b.publicationYear 
                    FROM Book b 
                    JOIN Borrow bo ON b.accessionNo = bo.accessionNo 
                    JOIN Author a ON bo.accessionNo = a.accessionNo 
                    WHERE borrowMemberId = '{0}')'''.format(memberId_entry.get())
        books_loaned = cursor.execute(members).fetchall()
        print(books_loaned)

        # Member does not have any books on loan.
        if books_loaned[0][0] == 0:
            root.title("INFO")
            root.geometry("800x400")

            error_label = tk.Label(root, text="INFO: You currently do not have any books on loan.", wraplength=700)
            error_label.config(font=(FONT, FONT_SIZE, STYLE))
            error_label.place(relx=0.5, rely=0.1, anchor="center")
            # back to main page button
            btn = tk.Button(root, text="Back to Reports Menu", command=root.destroy)
            btn.config(font=(FONT, FONT_SIZE, STYLE))
            btn.place(relx=0.5, rely=0.9, anchor="center")

        else:
            # ACTUALLY SELECT THE BOOKS THIS TIME
            members = '''SELECT b.accessionNo, b.title, a.author, b.isbn, b.publisher, b.publicationYear 
                    FROM Book b 
                    JOIN Borrow bo ON b.accessionNo = bo.accessionNo 
                    JOIN Author a ON bo.accessionNo = a.accessionNo 
                    WHERE borrowMemberId = "{0}" AND returnDate IS NULL'''.format(memberId_entry.get())
            books_for_member = cursor.execute(members).fetchall()
            my_books = []
            for n in range(len(books_for_member)):
                my_books.append(
                    (books_for_member[n][0], books_for_member[n][1], books_for_member[n][2], books_for_member[n][3],
                     books_for_member[n][4], books_for_member[n][5]))

            for book in my_books:
                tree.insert('', tk.END, values=book)

            def item_selected(event):
                for selected_item in tree.selection():
                    item = tree.item(selected_item)
                    record = item['values']
                    # show a message
                    showinfo(title='Information', message=','.join(record))

            tree.bind('<<TreeviewSelect>>', item_selected)

            tree.grid(row=0, column=0, sticky='nsew')

            # add a scrollbar
            scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.grid(row=0, column=1, sticky='ns')

            # back to main page button
            btn = tk.Button(root, text="Back to Reports Menu", command=root.destroy).grid(row=1, column=0)

    else:
        root.title("ERROR")
        root.geometry("800x400")
        root.configure(bg="#eb1e1e")

        error_label = tk.Label(root, text="ERROR: Invalid Membership ID!", bg="#eb1e1e", wraplength=700)
        error_label.config(font=(FONT, FONT_SIZE, STYLE))
        error_label.place(relx=0.5, rely=0.1, anchor="center")

        # back to main page button
        btn = tk.Button(root, text="Back to Reports Menu", command=root.destroy)
        btn.config(font=(FONT, FONT_SIZE, STYLE))
        btn.place(relx=0.5, rely=0.9, anchor="center")

    root.mainloop()


# Create New Windows for each Option.
def open1():
    global title_entry
    global authors_entry
    global isbn_entry
    global publisher_entry
    global publisher_year_entry

    # creates a new window rather than a pop-up
    top = tk.Toplevel()
    top.title("Book Search")
    top.geometry("1920x1080")

    # TOP HEADER
    header = tk.Label(top, text='Search based on one of the categories below:',
                      fg='black', bg='#c5e3e5', relief='raised', width=60, height=3)
    header.config(font=(FONT, FONT_SIZE, STYLE))
    header.place(relx=0.5, rely=0.09, anchor="center")

    # INPUT BOXES
    title = tk.Label(top, text="Title")
    title.config(font=(FONT, FONT_SIZE, STYLE))
    title.place(relx=0.25, rely=0.20, anchor="center")

    title_entry = tk.Entry(top, width=60)
    title_entry.place(relx=0.6, rely=0.20, width=600, height=40, anchor="center")
    title_entry.insert(0, "Book Name")  # default text inside input box

    authors = tk.Label(top, text="Authors")
    authors.config(font=(FONT, FONT_SIZE, STYLE))
    authors.place(relx=0.25, rely=0.30, anchor="center")

    authors_entry = tk.Entry(top, width=60)
    authors_entry.place(relx=0.6, rely=0.30, width=600, height=40, anchor="center")
    authors_entry.insert(0, "There can be multiple authors for a book.")  # default text inside input box

    isbn = tk.Label(top, text="ISBN")
    isbn.config(font=(FONT, FONT_SIZE, STYLE))
    isbn.place(relx=0.25, rely=0.40, anchor="center")

    isbn_entry = tk.Entry(top, width=60)
    isbn_entry.place(relx=0.6, rely=0.40, width=600, height=40, anchor="center")
    isbn_entry.insert(0, "ISBN Number")  # default text inside input box

    publisher = tk.Label(top, text="Publisher")
    publisher.config(font=(FONT, FONT_SIZE, STYLE))
    publisher.place(relx=0.25, rely=0.50, anchor="center")

    publisher_entry = tk.Entry(top, width=60)
    publisher_entry.place(relx=0.6, rely=0.50, width=600, height=40, anchor="center")
    publisher_entry.insert(0, "Random House, Penguin, Cengage, Springer, etc.")  # default text inside input box

    publisher_year = tk.Label(top, text="Publication Year")
    publisher_year.config(font=(FONT, FONT_SIZE, STYLE))
    publisher_year.place(relx=0.25, rely=0.6, anchor="center")

    publisher_year_entry = tk.Entry(top, width=60)
    publisher_year_entry.place(relx=0.6, rely=0.6, width=600, height=40, anchor="center")
    publisher_year_entry.insert(0, "Edition Year")  # default text inside input box

    # BOTTOM BUTTONS
    btn1 = tk.Button(top, text="Search Book", command=book_search)
    btn1.config(font=(FONT, FONT_SIZE, STYLE))
    btn1.place(relx=0.3, rely=0.8, anchor="center")

    btn2 = tk.Button(top, text="Back to Reports Menu", command=top.destroy)
    btn2.config(font=(FONT, FONT_SIZE, STYLE))
    btn2.place(relx=0.7, rely=0.8, anchor="center")

    top.mainloop()


## 12 Books on loan
def books_on_loan():
    engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'
                              .format(USERNAME, PASSWORD, HOST, PORT, DB), echo=False)

    # Create Cursor
    cursor = engine.connect()

    root = tk.Toplevel()
    root.title('Books on Loan Report')
    root.geometry('1225x245')

    columns = ('accessionNo', 'title', 'authors', 'isbn', 'publisher', 'publicationYear')

    tree = ttk.Treeview(root, columns=columns, show='headings')

    tree.heading('accessionNo', text='Accession Number')
    tree.heading('title', text='Title')
    tree.heading('authors', text='Authors')
    tree.heading('isbn', text='ISBN')
    tree.heading('publisher', text='Publisher')
    tree.heading('publicationYear', text='Publication Year')

    # check if there are loans
    loans_exist = '''SELECT EXISTS(SELECT * FROM Borrow WHERE returnDate IS NULL)'''
    result = cursor.execute(loans_exist).fetchall()

    if result[0][0] == 0:
        # no loans
        root.title("INFO")
        root.geometry("800x400")

        error_label = tk.Label(root, text="INFO: There are no books on loan in the system.", wraplength=700)
        error_label.config(font=(FONT, FONT_SIZE, STYLE))
        error_label.place(relx=0.5, rely=0.1, anchor="center")

        # back to main page button
        btn = tk.Button(root, text="Back to Reports Menu", command=root.destroy)
        btn.config(font=(FONT, FONT_SIZE, STYLE))
        btn.place(relx=0.5, rely=0.9, anchor="center")

    else:
    # Query 
        books_on_loan = '''SELECT b1.accessionNo, b2.title, a.author, b2.isbn, b2.publisher, b2.publicationYear 
                            FROM Borrow b1  
                            JOIN Book b2 
                            ON b1.accessionNo = b2.accessionNo 
                            JOIN Author a 
                            ON b2.accessionNo = a.accessionNo 
                            WHERE b1.returnDate IS NULL'''

        result = cursor.execute(books_on_loan).fetchall()

        loans = []
        for n in range(len(result)):
            # third element is an array
            loans.append((result[n][0], result[n][1], result[n][2], result[n][3], result[n][4], result[n][5]))

        for loan in loans:
            tree.insert('', tk.END, values=loan)

        def item_selected(event):
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                record = item['values']
                # show a message
                showinfo(title='Information', message=','.join(record))

        tree.bind('<<TreeviewSelect>>', item_selected)

        tree.grid(row=0, column=0, sticky='nsew')

        # add a scrollbar
        scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # back to main page button
        btn = tk.Button(root, text="Back to Reports Menu", command=root.destroy).grid(row=1, column=0)

    root.mainloop()


## 13 Books on reservation
def books_on_reservation():
    engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'
                              .format(USERNAME, PASSWORD, HOST, PORT, DB), echo=False)

    # Create Cursor
    cursor = engine.connect()

    root = tk.Toplevel()
    root.title('Books on Reservation Report')
    root.geometry('825x225')

    columns = ('accessionNo', 'title', 'memberId', 'name')

    tree = ttk.Treeview(root, columns=columns, show='headings')

    tree.heading('accessionNo', text='Accession Number')
    tree.heading('title', text='Title')
    tree.heading('memberId', text='Membership ID')
    tree.heading('name', text='Name')

    # check if there are reservations
    reservations_exist = '''SELECT EXISTS(SELECT * FROM Reservation)'''
    result = cursor.execute(reservations_exist).fetchall()

    if result[0][0] == 0:
        # no loans
        root.title("INFO")
        root.geometry("800x400")

        error_label = tk.Label(root, text="INFO: There are no reservations in the system.", wraplength=700)
        error_label.config(font=(FONT, FONT_SIZE, STYLE))
        error_label.place(relx=0.5, rely=0.1, anchor="center")

        # back to main page button
        btn = tk.Button(root, text="Back to Reports Menu", command=root.destroy)
        btn.config(font=(FONT, FONT_SIZE, STYLE))
        btn.place(relx=0.5, rely=0.9, anchor="center")

    else:
        # Query
        books_on_reservation = '''SELECT r.accessionNo, b.title, m.memberId, m.memberName FROM Reservation r 
                                INNER JOIN Members m on m.memberId = r.reservationMemberId 
                                INNER JOIN Book b on r.accessionNo = b.accessionNo'''
        result = cursor.execute(books_on_reservation).fetchall()

        reserved = []
        for n in range(len(result)):
            reserved.append((result[n][0], result[n][1], result[n][2], result[n][3]))

        for reserve in reserved:
            tree.insert('', tk.END, values=reserve)

        def item_selected(event):
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                record = item['values']
                # show a message
                showinfo(title='Information', message=','.join(record))

        tree.bind('<<TreeviewSelect>>', item_selected)

        tree.grid(row=0, column=0, sticky='nsew')

        # add a scrollbar
        scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # back to main page button
        btn = tk.Button(root, text="Back to Reports Menu", command=root.destroy).grid(row=1, column=0)

    root.mainloop()


## 14 Outstanding Fines
def outstanding_fines():
    engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'
                              .format(USERNAME, PASSWORD, HOST, PORT, DB), echo=False)

    # Create Cursor
    cursor = engine.connect()

    # TREEVIEW WIDGET
    root = tk.Toplevel()
    root.title('Members With Outstanding Fees')
    root.geometry('1025x225')

    columns = ('memberId', 'name', 'faculty', 'phoneNo', 'email')

    tree = ttk.Treeview(root, columns=columns, show='headings')

    tree.heading('memberId', text='Membership ID')
    tree.heading('name', text='Name')
    tree.heading('faculty', text='Faculty')
    tree.heading('phoneNo', text='Phone Number')
    tree.heading('email', text='Email Address')

    # check if there are fines
    fine_exists = '''SELECT EXISTS(SELECT * FROM Fine WHERE fineAmount <> 0)'''
    result = cursor.execute(fine_exists).fetchall()

    if result[0][0] == 0:
        # no outstanding fines
        root.title("INFO")
        root.geometry("800x400")

        error_label = tk.Label(root, text="INFO: There are no outstanding fines in the system.", wraplength=700)
        error_label.config(font=(FONT, FONT_SIZE, STYLE))
        error_label.place(relx=0.5, rely=0.1, anchor="center")

        # back to main page button
        btn = tk.Button(root, text="Back to Reports Menu", command=root.destroy)
        btn.config(font=(FONT, FONT_SIZE, STYLE))
        btn.place(relx=0.5, rely=0.9, anchor="center")

    else:
    # Query 
        outstanding_fines = '''SELECT m.memberId, m.memberName, m.faculty, m.phone, m.email 
                                FROM Fine f 
                                INNER JOIN Members m 
                                ON f.memberId = m.memberId
                                WHERE f.fineAmount <> 0'''

        result = cursor.execute(outstanding_fines).fetchall()

        fines = []
        for n in range(len(result)):
            fines.append((result[n][0], result[n][1], result[n][2], result[n][3], result[n][4]))

        for fine in fines:
            tree.insert('', tk.END, values=fine)

        def item_selected(event):
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                record = item['values']
                # show a message
                showinfo(title='Information', message=','.join(record))

        tree.bind('<<TreeviewSelect>>', item_selected)

        tree.grid(row=0, column=0, sticky='nsew')

        # add a scrollbar
        scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # back to main page button
        btn = tk.Button(root, text="Back to Reports Menu", command=root.destroy).grid(row=1, column=0)

    root.mainloop()


def open5():
    global memberId_entry
    # creates a new window rather than a pop-up
    top = tk.Toplevel()
    top.title("Books on Loan to Member")
    top.geometry("1920x1080")

    # TOP HEADER
    header = tk.Label(top, text="Books on Loan to Member", fg='black',
                      bg='#c5e3e5', relief='raised', width=60, height=3)
    header.config(font=(FONT, FONT_SIZE, STYLE))
    header.place(relx=0.5, rely=0.09, anchor="center")

    # INPUT BOXES
    memberId = tk.Label(top, text="Membership ID")
    memberId.config(font=(FONT, FONT_SIZE, STYLE))
    memberId.place(relx=0.35, rely=0.25, anchor="center")
    memberId_entry = tk.Entry(top, width=60)
    memberId_entry.place(relx=0.65, rely=0.25, width=660, height=40, anchor="center")
    memberId_entry.insert(0,
                          "A unique alphanumeric id that distinguishes every member")  # default text inside input box

    # BOTTOM BUTTONS
    btn1 = tk.Button(top, text="Search Member", command=mem_books)  # CREATE FUNCTION TO RETRIEVE TABLE
    btn1.config(font=(FONT, FONT_SIZE, STYLE))
    btn1.place(relx=0.3, rely=0.8, anchor="center")

    btn2 = tk.Button(top, text="Back to Reports Menu", command=top.destroy)
    btn2.config(font=(FONT, FONT_SIZE, STYLE))
    btn2.place(relx=0.7, rely=0.8, anchor="center")

    top.mainloop()


## slide 46
def reportsMenu():
    root = tk.Toplevel()
    root.title("Library System")
    root.geometry("1920x1080")

    # Top Half of Page
    label = tk.Label(root, text="Select one of the Options below", fg='black', bg='#c5e3e5', relief='raised', width=60,
                     height=3)
    label.config(font=(FONT, FONT_SIZE, STYLE))
    label.place(relx=0.5, rely=0.09, anchor="center")

    # Inserting an IMAGE on the left side of the page
    global my_img
    image = Image.open("pexels-photomix-company-95916.jpg")
    image = image.resize((400, 300), Image.ANTIALIAS)
    my_img = ImageTk.PhotoImage(image)
    img_canvas = tk.Canvas(root, width=300, height=250)
    img_canvas.place(relx=0.2, rely=0.50, anchor="w")
    img_canvas.create_image(50, 50, anchor="w", image=my_img)

    # Create buttons to initiate window opening for the various options
    booksearch_button = tk.Button(root, text="Book Search", command=open1)
    booksearch_button.config(font=(FONT, FONT_SIZE, STYLE))
    booksearch_button.place(relx=0.6, rely=0.3, anchor="center")

    booksonloan_button = tk.Button(root, text="Books on Loan", command=books_on_loan)
    booksonloan_button.config(font=(FONT, FONT_SIZE, STYLE))
    booksonloan_button.place(relx=0.6, rely=0.4, anchor="center")

    booksonreserve_button = tk.Button(root, text="Books On Reservation", command=books_on_reservation)
    booksonreserve_button.config(font=(FONT, FONT_SIZE, STYLE))
    booksonreserve_button.place(relx=0.6, rely=0.5, anchor="center")

    outstanding_fines_button = tk.Button(root, text="Outstanding Fines", command=outstanding_fines)
    outstanding_fines_button.config(font=(FONT, FONT_SIZE, STYLE))
    outstanding_fines_button.place(relx=0.6, rely=0.6, anchor="center")

    booksonloanToMember_button = tk.Button(root, text="Books on Loan to Member", command=open5)
    booksonloanToMember_button.config(font=(FONT, FONT_SIZE, STYLE))
    booksonloanToMember_button.place(relx=0.6, rely=0.7, anchor="center")

    # back to main page button
    btn = tk.Button(root, text="Back to Main Menu", bg='#c5e3e5', relief='raised', width=60, height=1,
                    command=root.destroy)
    btn.config(font=(FONT, FONT_SIZE, STYLE))
    btn.place(relx=0.5, rely=0.80, anchor="center")

    root.mainloop()
