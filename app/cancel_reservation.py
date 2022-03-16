import sqlalchemy as db
from tkinter import *
from PIL import Image, ImageTk

FONT = 'Arial'
FONT_SIZE = 25
SMALL_FONT_SIZE = 10
STYLE = 'bold'

USERNAME = "root"
PASSWORD = "Crunchyapples99"
HOST = "localhost"
PORT = 3306
DB = "Library"

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
cursor = engine.connect()

#slide 40 and success
def cancel_reservation_record():
    win = Tk()
    win.geometry("800x400")

    #check that the book is on reservation by member
    check_reservation = "SELECT * FROM Reservation WHERE accessionNo = '{}' AND reservationMemberId = '{}'".format(accession_no, member_id)
    reservation_record = cursor.execute(check_reservation).fetchall()
    
    if len(reservation_record) == 0:

        win.configure(bg = "#eb1e1e")

        win.title("ERROR")
        error_label = Label(win, text = "Member has no such reservation", bg = "#eb1e1e")
        error_label.config(font=(FONT, FONT_SIZE, STYLE))
        error_label.place(relx=0.5, rely=0.3, anchor="center")

        back_button = Button(win, text = "Back to Cancellation Function", command = win.destroy)
        back_button.config(font=(FONT, 20, STYLE))
        back_button.place(relx=0.5, rely=0.8, anchor='center')

        ## added this
        win.mainloop()
        
    else:

        win.configure(bg = "#b0f556")

        #delete reservation record
        delete_reservation = "DELETE FROM Reservation WHERE accessionNo = '{}' AND reservationMemberId = '{}'".format(accession_no, member_id)
        cursor.execute(delete_reservation)
        win.title("RESERVATION SUCCESSFULLY CANCELLED")

        success_label = Label(win, text = "Reservation has been successfully cancelled", bg = "#b0f556")
        success_label.config(font=(FONT, FONT_SIZE, STYLE))
        success_label.place(relx=0.5, rely=0.3, anchor="center")

        ok_button = Button(win, text = "Ok", command = win.destroy)
        ok_button.config(font=(FONT, 20, STYLE))
        ok_button.place(relx=0.5, rely=0.8, anchor='center')

        ## added this
        win.mainloop()

#slide 39
def confirmation_window():
    win = Tk()
    win.geometry("800x400")
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
        win.configure(bg = "#eb1e1e")

        error_label = Label(win, text = "ERROR: No such member and/or book exists", bg = "#eb1e1e")
        error_label.config(font=(FONT, FONT_SIZE, STYLE))
        error_label.place(relx=0.5, rely=0.3, anchor="center")

        back_button = Button(win, text = "Back to Reserve Function", command = win.destroy)
        back_button.config(font=(FONT, 20, STYLE))
        back_button.place(relx=0.5, rely=0.8, anchor='center')

        win.mainloop()

    #if no cancellation date is given
    if not cancel_date:

        win.configure(bg = "#eb1e1e")
        win.title("ERROR")
        
        error_label = Label(win, text = "ERROR: No cancellation date given", bg = "#eb1e1e")
        error_label.config(font=(FONT, FONT_SIZE, STYLE))
        error_label.place(relx=0.5, rely=0.3, anchor="center")

        back_button = Button(win, text = "Back to Reserve Function", command = win.destroy)
        back_button.config(font=(FONT, 20, STYLE))
        back_button.place(relx=0.5, rely=0.8, anchor='center')

        win.mainloop()

    #slide 39
    else:

        win.configure(bg = "#b0f556")

        member_name = member_name[0][1]
        book_title = book_title[0][1]
        
        confirmation_label = Label(win, text = "Confirm Cancel Reservation Details To Be Correct", bg = "#b0f556", wraplength=700)
        confirmation_label.config(font=(FONT, FONT_SIZE, STYLE))
        confirmation_label.place(relx=0.5, rely=0.1, anchor="center")
        
        accession_no_label = Label(win, text = "Accession Number: '{}'".format(accession_no), bg = "#b0f556")
        accession_no_label.config(font=(FONT, 15, STYLE))
        accession_no_label.place(relx=0.5, rely=0.25, anchor="center")
        
        book_title_label = Label(win, text = "Book Title: '{}'".format(book_title), bg = "#b0f556")
        book_title_label.config(font=(FONT, 15, STYLE))
        book_title_label.place(relx=0.5, rely=0.35, anchor="center")

        member_id_label = Label(win, text = "Membership ID: '{}'".format(member_id), bg = "#b0f556")
        member_id_label.config(font=(FONT, 15, STYLE))
        member_id_label.place(relx=0.5, rely=0.45, anchor="center")
        
        member_name_label = Label(win, text = "Member Name: '{}'".format(member_name), bg = "#b0f556")
        member_name_label.config(font=(FONT, 15, STYLE))
        member_name_label.place(relx=0.5, rely=0.55, anchor="center")
        
        cancel_date_label = Label(win, text = "Cancellation Date: '{}'".format(cancel_date), bg = "#b0f556")
        cancel_date_label.config(font=(FONT, 15, STYLE))
        cancel_date_label.place(relx=0.5, rely=0.65, anchor="center")

        confirm_button = Button(win, text = "Confirm Cancellation", command = lambda: [cancel_reservation_record(), win.destroy()])
        confirm_button.config(font=(FONT, 15, STYLE))
        confirm_button.place(relx=0.3, rely=0.85, anchor="center")

        back_button = Button(win, text = "Back to Cancellation Function", command = win.destroy)
        back_button.config(font=(FONT, 15, STYLE))
        back_button.place(relx=0.7, rely=0.85, anchor="center")

        win.mainloop()

def cancel_reservation_details():
    win = Toplevel()
    win.geometry("1920x1080")

    win.title("Cancel a Reservation")

    image = Image.open("bg1.jpg")
    image = image.resize((1920, 1080))

    bg = ImageTk.PhotoImage(image)
    canvas1 = Canvas(win, width = 1920, height = 1080)
    canvas1.pack(fill = "both", expand =  True)
    canvas1.create_image(0, 0, image = bg, anchor = "nw")


    #creating the fields + labels for slide 38
    global accession_no_field
    global membership_id_field
    global cancel_date_field

    # TOP HEADER
    header = Label(win, text='To Cancel a Reservation, Please Enter Information Below:',
                      fg='black', bg='#c5e3e5', relief='raised', width=60, height=3)
    header.config(font=(FONT, FONT_SIZE, STYLE))
    header.place(relx=0.5, rely=0.09, anchor="center")
    
    accession_no_field = Entry(win, width=60)
    accession_no_field.place(relx=0.6, rely=0.35, width=600, height=40, anchor="center")

    accession_no_label = Label(win, text = "Accession Number", bg = "#FFE45E")
    accession_no_label.config(font=(FONT, FONT_SIZE, STYLE))
    accession_no_label.place(relx=0.25, rely=0.35, anchor="center")

    membership_id_field = Entry(win, width=60)
    membership_id_field.place(relx=0.6, rely=0.45, width=600, height=40, anchor="center")

    membership_id_label = Label(win, text = "Membership ID", bg = "#FFE45E")
    membership_id_label.config(font=(FONT, FONT_SIZE, STYLE))
    membership_id_label.place(relx=0.25, rely=0.45, anchor="center")

    cancel_date_field = Entry(win, width=60)
    cancel_date_field.place(relx=0.6, rely=0.55, width=600, height=40, anchor="center")

    cancel_date_label = Label(win, text = "Cancellation Date", bg = "#FFE45E")
    cancel_date_label.config(font=(FONT, FONT_SIZE, STYLE))
    cancel_date_label.place(relx=0.25, rely=0.55, anchor="center")

    cancel_button = Button(win, text = "Cancel Reservation", command = confirmation_window)
    cancel_button.config(font=(FONT, FONT_SIZE, STYLE))
    cancel_button.place(relx=0.3, rely=0.8, anchor="center")

    back_button = Button(win, text = "Back to Reservations Menu", command = win.destroy)
    back_button.config(font=(FONT, FONT_SIZE, STYLE))
    back_button.place(relx=0.7, rely=0.8, anchor="center")

    win.mainloop()



