import sqlalchemy as db
from tkinter import *
from datetime import *

FONT = 'Arial'
FONT_SIZE = 25
SMALL_FONT_SIZE = 10
STYLE = 'bold'

USERNAME = "root"
PASSWORD = "" ## enter password
HOST = "localhost"
PORT = 3306
DB = "Library"

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
cursor = engine.connect()

#slides 36, 37 and success
def add_reservation_record():
    win = Tk()

    #check that the book is not on loan or reserved
    check_on_loan = "SELECT * FROM Borrow WHERE accessionNo = '{}'".format(accession_no)
    loan_record = cursor.execute(check_on_loan).fetchall()
    on_loan = False

    #if there is a loan record, check if it has been returned
    if loan_record:
        for record in loan_record:
            return_date = record[3]
            if return_date == None:
                on_loan = True
    
    check_on_reserve = "SELECT * FROM Reservation WHERE accessionNo = '{}'".format(accession_no)
    on_reserve = cursor.execute(check_on_reserve).fetchall()
    
    if not on_loan and not on_reserve:
        #check if member has any outstanding fines
        check_fine = "SELECT * FROM Fine WHERE memberId = '{}'".format(member_id)
        fine_records = cursor.execute(check_fine).fetchall()
        no_fine = True
        if fine_records:
            for record in fine_records:
                fine_amount = record[1]
                if fine_amount != 0:
                    no_fine = False

        if no_fine:
            #check only 0 or 1 book reserved
            check_reservations = "SELECT * FROM Reservation WHERE reservationMemberId = '{}'".format(member_id)
            reservations_made = len(cursor.execute(check_reservations).fetchall())
                
            if reservations_made <= 1:
                #add reservation
                insert_reservation = "INSERT INTO Reservation VALUES ('{}', '{}', '{}')".format(accession_no, reserve_date, member_id)
                cursor.execute(insert_reservation)
                win.title("BOOK SUCCESSFULLY RESERVED")
                success_label = Label(win, text = "Reservation successfully made")
                success_label.grid(row = 0, column = 0)
                ok_button = Button(win, text = "Ok", command = win.destroy)
                ok_button.grid(row = 1, column = 0)

            else:
                win.title("ERROR")
                error_label = Label(win, text = "ERROR: Member currently has 2 books on reservation")
                error_label.grid(row = 0, column = 0)
                back_button = Button(win, text = "Back to Reserve Function", command = win.destroy)
                back_button.grid(row = 1, column = 0)

        else:
            win.title("ERROR")
            fine_amount = got_fine[0][1]
            error_label = Label(win, text = "ERROR: Member has an outstanding fine of ${}".format(fine_amount))
            error_label.grid(row = 0, column = 0)
            back_button = Button(win, text = "Back to Reserve Function", command = win.destroy)
            back_button.grid(row = 1, column = 0)
    else:
        win.title("ERROR")
        error_label = Label(win, text = "ERROR: Book is either on loan or already reserved")
        error_label.grid(row = 0, column = 0)
        back_button = Button(win, text = "Back to Reserve Function", command = win.destroy)
        back_button.grid(row = 1, column = 0)

#slide 35
def confirmation_window():
    win = Tk()

    #store the input into variables
    global accession_no
    global member_id
    global reserve_date
    
    accession_no = accession_no_field.get()
    member_id = membership_id_field.get()
    reserve_date = reserve_date_field.get()

    #get member name and book title
    get_member_name = "SELECT * FROM Members WHERE memberId = '{}'".format(member_id)
    member_name = cursor.execute(get_member_name).fetchall()
    get_book_title = "SELECT * FROM Book WHERE accessionNo = '{}'".format(accession_no)
    book_title = cursor.execute(get_book_title).fetchall()

    #invalid member id or invalid accession_no
    if not member_name or not book_title:
        win.title("ERROR")
        
        error_label = Label(win, text = "ERROR: No such member and/or book exists")
        error_label.grid(row = 0, column = 0)
        back_button = Button(win, text = "Back to Reserve Function", command = win.destroy)
        back_button.grid(row = 1, column = 0)

        win.mainloop()

    #no reserve date entered
    if not reserve_date:
        win.title("ERROR")
        
        error_label = Label(win, text = "ERROR: Reserve date not entered")
        error_label.grid(row = 0, column = 0)
        back_button = Button(win, text = "Back to Reserve Function", command = win.destroy)
        back_button.grid(row = 1, column = 0)

        win.mainloop()

    #slide 35
    else:
        win.title("Confirmation of Reservation")
        
        member_name = member_name[0][1]
        book_title = book_title[0][1]
        
        confirmation_label = Label(win, text = "Confirm Reservation Details To Be Correct")
        confirmation_label.grid(row = 0, column = 0)
        
        accession_no_label = Label(win, text = "Accession Number: '{}'".format(accession_no))
        accession_no_label.grid(row = 1, column = 0)
        
        book_title_label = Label(win, text = "Book Title: '{}'".format(book_title))
        book_title_label.grid(row = 2, column = 0)

        member_id_label = Label(win, text = "Membership ID: '{}'".format(member_id))
        member_id_label.grid(row = 3, column = 0)
        
        member_name_label = Label(win, text = "Member Name: '{}'".format(member_name))
        member_name_label.grid(row = 4, column = 0)
        
        reserve_date_label = Label(win, text = "Reserve Date: '{}'".format(reserve_date))
        reserve_date_label.grid(row = 5, column = 0)

        confirm_button = Button(win, text = "Confirm Reservation", command = lambda: [add_reservation_record(), win.destroy()])
        confirm_button.grid(row = 6, column = 0)

        back_button = Button(win, text = "Back to Reserve Function", command = win.destroy)
        back_button.grid(row = 6, column = 1)

        win.mainloop()

def reservation_details():
    win = Toplevel()
    win.title("Reserve a Book")
    win.geometry("1920x1080")

	image = Image.open("bg1.jpg")
	image = image.resize((1300, 650))

	bg = ImageTk.PhotoImage(image)
	canvas1 = Canvas(win, width = 1920, height = 1080)
	canvas1.pack(fill = "both", expand =  True)
	canvas1.create_image(0, 0, image = bg, anchor = "nw")

    #creating the fields + labels for slide 34
    global accession_no_field
    global membership_id_field
    global reserve_date_field
    
    instructions = Label(win, text='To Reserve a Book, Please Enter Information Below:', fg='black', bg='#c5e3e5', relief='raised', width=60, height=3)
    instructions.config(font=(FONT, FONT_SIZE, STYLE))
    instructions.place(relx=0.5, rely=0.09, anchor="center")

    accession_no_label = Label(win, text = "Accession Number")
    accession_no_label.config(font=(FONT, FONT_SIZE, STYLE))
    accession_no_label.place(relx=0.35, rely=0.35, anchor="center")
    accession_no_field = Entry(win, width = 60)
    accession_no_field.place(relx=0.65, rely=0.35, width = 660, height = 40, anchor="center")

    membership_id_label = Label(win, text = "Membership ID")
    membership_id_label.config(font=(FONT, FONT_SIZE, STYLE))
    membership_id_label.place(relx=0.35, rely=0.45, anchor="center")
    membership_id_field = Entry(win, width = 60)
    membership_id_field.place(relx=0.65, rely=0.45, width = 660, height = 40, anchor="center")

    reserve_date_label = Label(win, text = "Reserve Date")
    reserve_date_label.config(font=(FONT, FONT_SIZE, STYLE))
    reserve_date_label.place(relx=0.35, rely=0.55, anchor="center")
    reserve_date_field = Entry(win, width = 60)
    reserve_date_field.place(relx=0.65, rely=0.55, width = 660, height = 40, anchor="center")

    reserve_button = Button(win, text = "Reserve Book", command = confirmation_window)
    reserve_button.config(font=(FONT, FONT_SIZE, STYLE))
    reserve_button.place(relx=0.3, rely=0.8, anchor="center")

    back_button = Button(win, text = "Back to Reservations Menu", command = win.destroy)
    back_button.config(font=(FONT, FONT_SIZE, STYLE))
    back_button.place(relx=0.7, rely=0.8, anchor="center")



    win.mainloop()





