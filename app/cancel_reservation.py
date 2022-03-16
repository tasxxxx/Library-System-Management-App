import sqlalchemy as db
from tkinter import *

USERNAME = "root"
PASSWORD = "Dcmmq9ck5s24!"
HOST = "localhost"
PORT = 3306
DB = "Library"

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
cursor = engine.connect()
#metadata = db.MetaData()

#slide 40 and success
def cancel_reservation_record():
    win = Tk()

    #check that the book is on reservation by member
    check_reservation = "SELECT * FROM Reservation WHERE accessionNo = '{}' AND reservationMemberId = '{}'".format(accession_no, member_id)
    reservation_record = cursor.execute(check_reservation).fetchall()
    
    if len(reservation_record) == 0:
        win.title("ERROR")
        error_label = Label(win, text = "Member has no such reservation")
        error_label.grid(row = 0, column = 0)
        back_button = Button(win, text = "Back to Cancellation Function", command = win.destroy)
        back_button.grid(row = 1, column = 0)
        
    else:
        #delete reservation record
        delete_reservation = "DELETE FROM Reservation WHERE accessionNo = '{}' AND reservationMemberId = '{}'".format(accession_no, member_id)
        cursor.execute(delete_reservation)
        win.title("RESERVATION SUCCESSFULLY CANCELLED")
        success_label = Label(win, text = "Reservation has been successfully cancelled")
        success_label.grid(row = 0, column = 0)
        ok_button = Button(win, text = "Ok", command = win.destroy)
        ok_button.grid(row = 1, column = 0)

#slide 39
def confirmation_window():
    win = Tk()
    win.title("Confirmation of Cancelling Reservation")

    #store the input into variables
    global accession_no
    global member_id
    global cancel_date
    
    accession_no = accession_no_field.get()
    member_id = membership_id_field.get()
    cancel_date = cancel_date_field.get()

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

    #if no cancellation date is given
    if not cancel_date:
        win.title("ERROR")
        
        error_label = Label(win, text = "ERROR: No cancellation date given")
        error_label.grid(row = 0, column = 0)
        back_button = Button(win, text = "Back to Reserve Function", command = win.destroy)
        back_button.grid(row = 1, column = 0)

        win.mainloop()

    #slide 39
    else:
        member_name = member_name[0][1]
        book_title = book_title[0][1]
        
        confirmation_label = Label(win, text = "Confirm Cancel Reservation Details To Be Correct")
        confirmation_label.grid(row = 0, column = 0)
        
        accession_no_label = Label(win, text = "Accession Number: '{}'".format(accession_no))
        accession_no_label.grid(row = 1, column = 0)
        
        book_title_label = Label(win, text = "Book Title: '{}'".format(book_title))
        book_title_label.grid(row = 2, column = 0)

        member_id_label = Label(win, text = "Membership ID: '{}'".format(member_id))
        member_id_label.grid(row = 3, column = 0)
        
        member_name_label = Label(win, text = "Member Name: '{}'".format(member_name))
        member_name_label.grid(row = 4, column = 0)
        
        cancel_date_label = Label(win, text = "Cancellation Date: '{}'".format(cancel_date))
        cancel_date_label.grid(row = 5, column = 0)

        confirm_button = Button(win, text = "Confirm Cancellation", command = lambda: [cancel_reservation_record(), win.destroy()])
        confirm_button.grid(row = 6, column = 0)

        back_button = Button(win, text = "Back to Cancellation Function", command = win.destroy)
        back_button.grid(row = 6, column = 2)

        win.mainloop()

def cancel_reservation_details():
    win = Tk()
    win.title("Cancel a Reservation")

    #creating the fields + labels for slide 38
    global accession_no_field
    global membership_id_field
    global cancel_date_field
    
    accession_no_field = Entry(win, width = 30)
    accession_no_field.grid(row = 0, column = 1)
    accession_no_label = Label(win, text = "Accession Number")
    accession_no_label.grid(row = 0, column = 0)

    membership_id_field = Entry(win, width = 30)
    membership_id_field.grid(row = 1, column = 1)
    membership_id_label = Label(win, text = "Membership ID")
    membership_id_label.grid(row = 1, column = 0)

    cancel_date_field = Entry(win, width = 30)
    cancel_date_field.grid(row = 2, column = 1)
    cancel_date_label = Label(win, text = "Cancellation Date")
    cancel_date_label.grid(row = 2, column = 0)

    cancel_button = Button(win, text = "Cancel Reservation", command = confirmation_window)
    cancel_button.grid(row = 3, column = 0)

    back_button = Button(win, text = "Back to Reservations Menu", command = win.destroy)
    back_button.grid(row = 3, column = 3)

    win.mainloop()



