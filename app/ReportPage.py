import sqlalchemy as db
import tkinter as tk
import pandas as pd 
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import showinfo

# 11 FUNCTION FOR BOOK SEACRH
def book_search():
    # Create a database or connect to one
    USERNAME = "root"
    PASSWORD = "Hoepeng.0099"
    HOST = "localhost"
    PORT = 3306
    DB = "Library"

    engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'
                           .format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
    
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
            error_label = tk.Label(root, text = "ERROR: You may only enter one word per search field. Please try again.")
            error_label.grid(row = 0, column = 0)
            # back to main page button
            btn = tk.Button(root, text="Back to Reports Menu",command=root.destroy).grid(row=1, column=0)
    else:
        statement = '''SELECT b.accessionNo, b.title, a.author, b.isbn, b.publisher, b.publicationYear 
                    FROM Book b 
                    JOIN Author a ON b.accessionNo = a.accessionNo'''
        
        add_on_condition = ""
        CLAUSE = ["WHERE", "AND"]
        rotation = 0 
        
        # If there is a field entry for author:
        if len(a) > 0: 
            author_condition = " WHERE a.accessionNo IN (SELECT accessionNo FROM Author WHERE author REGEXP '(^|[[:space:]]){}([[:space:]]|$)')".format(a)
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
    btn = tk.Button(root, text="Back to Reports Menu",command=root.destroy).grid(row=1,column=0)

    root.mainloop()

# 15 FUNCTION TO SHOW BOOKS ON LOAN PER MEMBER
def mem_books():
    
     # Create a database or connect to one
    USERNAME = "root"
    PASSWORD = "Hoepeng.0099" # your password
    HOST = "localhost"
    PORT = 3306
    DB = "Library"

    engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'
                           .format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
    
    # Create Cursor
    cursor = engine.connect()
    
    root = tk.Toplevel()
    root.title('Books on Loan to Member')
    root.geometry('1425x225')

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
            error_label = tk.Label(root, text = "INFO: You currently do not have any books on loan.")
            error_label.grid(row = 0, column = 0)
            # back to main page button
            btn = tk.Button(root, text="Back to Reports Menu",command=root.destroy).grid(row=1, column=0)

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
                my_books.append((books_for_member[n][0], books_for_member[n][1], books_for_member[n][2], books_for_member[n][3],
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
            btn = tk.Button(root, text="Back to Reports Menu",command=root.destroy).grid(row=1, column=0)

    else:
        root.title("ERROR")
        error_label = tk.Label(root, text = "ERROR: Invalid Membership ID!")
        error_label.grid(row = 0, column = 0)
            
        # back to main page button
        btn = tk.Button(root, text="Back to Reports Menu",command=root.destroy).grid(row=1, column=0)
        
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
    
    # TOP HEADER
    frame = tk.LabelFrame(top, padx=5, pady=5)
    frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
    label = tk.Label(frame, text="Search based on one of the categories below:").pack()
    
    # INPUT BOXES
    title = tk.Label(top, text="Title").grid(row=1, column=0)
    title_entry = tk.Entry(top, width=30, bd=3)
    title_entry.grid(row=1, column=1)
    title_entry.insert(0, "Book Name") # default text inside input box

    authors = tk.Label(top, text="Authors").grid(row=2, column=0)
    authors_entry = tk.Entry(top, width=30, bd=3)
    authors_entry.grid(row=2, column=1)
    authors_entry.insert(0, "There can be multiple authors for a book.") # default text inside input box
    
    isbn = tk.Label(top, text="ISBN").grid(row=3, column=0)
    isbn_entry = tk.Entry(top, width=30, bd=3)
    isbn_entry.grid(row=3, column=1)
    isbn_entry.insert(0, "ISBN Number") # default text inside input box
    
    publisher = tk.Label(top, text="Publisher").grid(row=4, column=0)
    publisher_entry = tk.Entry(top, width=30, bd=3)
    publisher_entry.grid(row=4, column=1)
    publisher_entry.insert(0, "Random House, Penguin, Cengage, Springer, etc.") # default text inside input box

    publisher_year = tk.Label(top, text="Publication Year").grid(row=5, column=0)
    publisher_year_entry = tk.Entry(top, width=30, bd=3)
    publisher_year_entry.grid(row=5, column=1)
    publisher_year_entry.insert(0, "Edition Year") # default text inside input box
    
    # BOTTOM BUTTONS
    btn1 = tk.Button(top, text="Search Book",command=book_search) # CREATE FUNCTION TO RETRIEVE TABLE
    btn1.grid(row=6, column=0)
    btn2 = tk.Button(top, text="Back to Reports Menu",command=top.destroy)
    btn2.grid(row=6, column=2)
    
    top.mainloop()

## 12 Books on loan
def books_on_loan():

    # Create a database or connect to one
    USERNAME = "root"
    PASSWORD = "Hoepeng.0099"
    HOST = "localhost"
    PORT = 3306
    DB = "Library"

    engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'
                           .format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
    
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
    btn = tk.Button(root, text="Back to Reports Menu",command=root.destroy).grid(row=1, column=0)

    root.mainloop()


## 13 Books on reservation
def books_on_reservation():
    
    # Create a database or connect to one
    USERNAME = "root"
    PASSWORD = "Hoepeng.0099"
    HOST = "localhost"
    PORT = 3306
    DB = "Library"

    engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'
                           .format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
    
    # Create Cursor
    cursor = engine.connect()
    
    # Query 
    books_on_reservation = '''SELECT r.accessionNo, b.title, m.memberId, m.memberName FROM Reservation r 
                            INNER JOIN Members m on m.memberId = r.reservationMemberId 
                            INNER JOIN Book b on r.accessionNo = b.accessionNo'''
    result = cursor.execute(books_on_reservation).fetchall()
    
    root = tk.Toplevel()
    root.title('Books on Reservation Report')
    root.geometry('825x225')

    columns = ('accessionNo', 'title', 'memberId', 'name')

    tree = ttk.Treeview(root, columns=columns, show='headings')

    tree.heading('accessionNo', text='Accession Number')
    tree.heading('title', text='Title')
    tree.heading('memberId', text='Membership ID')
    tree.heading('name', text='Name')

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
    btn = tk.Button(root, text="Back to Reports Menu",command=root.destroy).grid(row=1, column=0)

    root.mainloop()


## 14 Outstanding Fines
def outstanding_fines():
    
    # Create a database or connect to one
    USERNAME = "root"
    PASSWORD = "Hoepeng.0099"
    HOST = "localhost"
    PORT = 3306
    DB = "Library"

    engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'
                           .format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
    
    # Create Cursor
    cursor = engine.connect()
    
    # Query 
    outstanding_fines = '''SELECT m.memberId, m.memberName, m.faculty, m.phone, m.email 
                            FROM Fine f 
                            INNER JOIN Members m 
                            ON f.memberId = m.memberId
                            WHERE f.fineAmount <> 0'''

    result = cursor.execute(outstanding_fines).fetchall()

    # TREEVIEW WIDGET
    root = tk.Tk()
    root.title('Members With Outstanding Fees')
    root.geometry('1025x225')

    columns = ('memberId', 'name', 'faculty', 'phoneNo', 'email')

    tree = ttk.Treeview(root, columns=columns, show='headings')

    tree.heading('memberId', text='Membership ID')
    tree.heading('name', text='Name')
    tree.heading('faculty', text='Faculty')
    tree.heading('phoneNo', text='Phone Number')
    tree.heading('email', text='Email Address')

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
    btn = tk.Button(root, text="Back to Reports Menu",command=root.destroy).grid(row=1, column=0)

    root.mainloop()
    
def open5():
                   
    global memberId_entry
    # creates a new window rather than a pop-up
    top = tk.Toplevel()
    top.title("Books on Loan to Member")
    
    # TOP HEADER
    frame = tk.LabelFrame(top, padx=5, pady=5)
    frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
    label = tk.Label(frame, text="Books on Loan to Member").pack()
    
    # INPUT BOXES
    memberId = tk.Label(top, text="Membership ID").grid(row=1, column=0)
    memberId_entry = tk.Entry(top, width=30, bd=3)
    memberId_entry.grid(row=1, column=1)
    memberId_entry.insert(0, "A unique alphanumeric id that distinguishes every member") # default text inside input box
    
    # BOTTOM BUTTONS
    btn1 = tk.Button(top, text="Search Member",command=mem_books) # CREATE FUNCTION TO RETRIEVE TABLE
    btn1.grid(row=2, column=0)
    btn2 = tk.Button(top, text="Back to Reports Menu",command=top.destroy)
    btn2.grid(row=2, column=2)
    
    top.mainloop()
    
## slide 46
def reportsMenu():

    root = tk.Toplevel()
    root.title("Library System")
    root.geometry("600x410")

    # Top Half of Page
    frame = tk.LabelFrame(root, padx=5, pady=5)
    frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
    label = tk.Label(frame, text="Select one of the Options below").pack()

    # Inserting an IMAGE on the left side of the page 
    global my_img
    image = Image.open("pexels-photomix-company-95916.jpg")
    image = image.resize((400, 300), Image.ANTIALIAS)
    my_img = ImageTk.PhotoImage(image)
    my_label = tk.Label(image=my_img)
    my_label.grid(row = 1, column = 0, rowspan=5, padx=10, pady=10)

    # Create buttons to initiate window opening for the various options
    booksearch_button = tk.Button(root, text="Book Search", command=open1)
    booksearch_button.grid(row=1, column=1, columnspan=2)
    booksonloan_button = tk.Button(root, text="Books on Loan", command=books_on_loan)
    booksonloan_button.grid(row=2, column=1, columnspan=2)
    booksonreserve_button = tk.Button(root, text="Books On Reservation", command=books_on_reservation)
    booksonreserve_button.grid(row=3, column=1, columnspan=2)
    outstanding_fines_button = tk.Button(root, text="Outstanding Fines", command=outstanding_fines)
    outstanding_fines_button.grid(row=4, column=1, columnspan=2)
    booksonloanToMember_button = tk.Button(root, text="Books on Loan to Member", command=open5)
    booksonloanToMember_button.grid(row=5, column=1, columnspan=2)
    # back to main page button
    btn = tk.Button(root, text="Back to Main Menu",command=root.destroy).grid(row=6, column=1)

    root.mainloop()


