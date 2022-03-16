import sqlalchemy as db
from tkinter import *
from datetime import *

USERNAME = "root"
PASSWORD = "Hoepeng.0099"
HOST = "localhost"
PORT = 3306
DB = "Library"

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
cursor = engine.connect()

#slide 44, 45 and success
def complete_payment():
    win = Tk()

    check_fine = "SELECT * FROM Fine WHERE memberId = '{}'".format(member_id)
    got_fine = cursor.execute(check_fine).fetchall()

    #if got fine
    if got_fine: 
        fine_amount = got_fine[0][1]

        #if correct amount
        if fine_amount == int(payment_amount):
            #add payment record
            insert_payment = "INSERT INTO Payment VALUES ('{}', '{}')".format(member_id, payment_date)
            cursor.execute(insert_payment)

            #delete fine record
            delete_fine = "DELETE FROM Fine WHERE memberId = '{}'".format(member_id)
            cursor.execute(delete_fine)
            
            win.title("FINE PAID SUCCESSFULLY")
            success_label = Label(win, text = "Fine successfully paid")
            success_label.grid(row = 0, column = 0)
            ok_button = Button(win, text = "Ok", command = win.destroy)
            ok_button.grid(row = 1, column = 0)

        else:
            win.title("ERROR")
            error_label = Label(win, text = "ERROR: Incorrect fine payment amount")
            error_label.grid(row = 0, column = 0)
            back_button = Button(win, text = "Back to Payment Function", command = win.destroy)
            back_button.grid(row = 1, column = 0)

    else:
        win.title("ERROR")
        error_label = Label(win, text = "ERROR: Member has no fine")
        error_label.grid(row = 0, column = 0)
        back_button = Button(win, text = "Back to Payment Function", command = win.destroy)
        back_button.grid(row = 1, column = 0)

#slide 43
def confirmation_window():
    win = Tk()
    
    #store the input into variables
    global member_id
    global payment_date
    global payment_amount
    
    member_id = membership_id_field.get()
    payment_date = payment_date_field.get()
    payment_amount = payment_amount_field.get()

    #check if member exists
    get_member_name = "SELECT * FROM Members WHERE memberId = '{}'".format(member_id)
    member_name = cursor.execute(get_member_name).fetchall()

    #invalid member id
    if not member_name:
        win.title("ERROR")
        
        error_label = Label(win, text = "ERROR: No such member")
        error_label.grid(row = 0, column = 0)
        back_button = Button(win, text = "Back to Payment Function", command = win.destroy)
        back_button.grid(row = 1, column = 0)

        win.mainloop()

    #no payment date or payment amount
    if not payment_date or not payment_amount:
        win.title("ERROR")
        
        error_label = Label(win, text = "ERROR: Missing fields")
        error_label.grid(row = 0, column = 0)
        back_button = Button(win, text = "Back to Payment Function", command = win.destroy)
        back_button.grid(row = 1, column = 0)

        win.mainloop()

    #slide 35
    else:
        win.title("Confirmation of Payment Details")
        
        confirmation_label = Label(win, text = "Confirm Payment Details To Be Correct")
        confirmation_label.grid(row = 0, column = 0)

        payment_due_label = Label(win, text = "Payment Due: ${}".format(payment_amount))
        payment_due_label.grid(row = 1, column = 0)

        member_id_label = Label(win, text = "Member ID: {}".format(member_id))
        member_id_label.grid(row = 1, column = 2)

        payment_exact_label = Label(win, text = "Exact Fee Only")
        payment_exact_label.grid(row = 2, column = 0)

        payment_date_label = Label(win, text = "Payment Date: {}".format(payment_date))
        payment_date_label.grid(row = 2, column = 2)

        confirm_button = Button(win, text = "Confirm Payment", command = lambda: [complete_payment(), win.destroy()])
        confirm_button.grid(row = 6, column = 0)

        back_button = Button(win, text = "Back to Payment Function", command = win.destroy)
        back_button.grid(row = 6, column = 2)

        win.mainloop()

#slide 42
def fine_details():
    win = Tk()
    win.title("Pay a Fine")

    #creating the fields + labels for slide 34
    global membership_id_field
    global payment_date_field
    global payment_amount_field

    membership_id_field = Entry(win, width = 30)
    membership_id_field.grid(row = 0, column = 1)
    membership_id_label = Label(win, text = "Membership ID")
    membership_id_label.grid(row = 0, column = 0)

    payment_date_field = Entry(win, width = 30)
    payment_date_field.grid(row = 1, column = 1)
    payment_date_label = Label(win, text = "Payment Date")
    payment_date_label.grid(row = 1, column = 0)

    payment_amount_field = Entry(win, width = 30)
    payment_amount_field.grid(row = 2, column = 1)
    payment_amount_label = Label(win, text = "Payment Amount")
    payment_amount_label.grid(row = 2, column = 0)

    pay_button = Button(win, text = "Pay Fine", command = confirmation_window)
    pay_button.grid(row = 3, column = 0)

    back_button = Button(win, text = "Back to Fines Menu", command = win.destroy)
    back_button.grid(row = 3, column = 3)

    win.mainloop()
