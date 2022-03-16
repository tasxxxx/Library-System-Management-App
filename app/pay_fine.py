import sqlalchemy as db
from tkinter import *
from datetime import *
from sqlalchemy.exc import IntegrityError, DataError, OperationalError
from PIL import ImageTk, Image

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

#slide 44, 45 and success
def complete_payment():
    win = Tk()
    win.geometry("800x400")

    check_fine = "SELECT * FROM Fine WHERE memberId = '{}'".format(member_id)
    got_fine = cursor.execute(check_fine).fetchall()

    try:

        #if got fine
        if got_fine: 
            fine_amount = got_fine[0][1]

            #if correct amount
            if fine_amount == int(payment_amount):
                #add payment record
                insert_payment = "INSERT INTO Payment VALUES ('{}', '{}')".format(member_id, payment_date)
                cursor.execute(insert_payment)

                #delete fine record
                # update as of 16/3 5.31pm: edited for fine record to be updated to 0 instead of deleted
                zeroed_fine = "UPDATE Fine SET fineAmount = 0 WHERE memberId = '{}'".format(member_id)
                cursor.execute(zeroed_fine)
                
                win.title("FINE PAID SUCCESSFULLY")
                success_label = Label(win, text = "Fine successfully paid")
                success_label.place(relx=0.5, rely=0.3, anchor='center')
                ok_button = Button(win, text = "Ok", command = win.destroy)
                ok_button.config(font=(FONT, 20, STYLE))
                ok_button.place(relx=0.5, rely=0.8, anchor='center')

            else:
                win.title("ERROR")
                win.configure(bg = "#eb1e1e")

                error_label = Label(win, text = "Error!", bg = "#eb1e1e")
                error_label.config(font=(FONT, 20, STYLE))
                error_label.place(relx=0.5, rely=0.15, anchor="center")

                error_label2 = Label(win, text = "Incorrect fine payment amount.", bg = "#eb1e1e")
                error_label2.config(font=(FONT, SMALL_FONT_SIZE, STYLE))
                error_label.place(relx=0.5, rely=0.3, anchor="center")
                
                back_button = Button(win, text = "Back to Payment Function", command = win.destroy)
                back_button.config(font=(FONT, 20, STYLE))
                back_button.place(relx=0.5, rely=0.8, anchor='center')

        else:
            win.title("ERROR")
            win.configure(bg = "#eb1e1e")

            error_label = Label(win, text = "Error! ", bg = "#eb1e1e")
            error_label.config(font=(FONT, 20, STYLE))
            error_label.place(relx=0.5, rely=0.15, anchor="center")

            error_label2 = Label(win, text = "Member has no fine.", bg = "#eb1e1e")
            error_label2.config(font=(FONT, SMALL_FONT_SIZE, STYLE))
            error_label.place(relx=0.5, rely=0.3, anchor="center")

            back_button = Button(win, text = "Back to Payment Function", command = win.destroy)
            back_button.config(font=(FONT, 20, STYLE))
            back_button.place(relx=0.5, rely=0.8, anchor='center')

    except (ValueError, IntegrityError, DataError, OperationalError):
            label1 = Label(win, text="Error!", bg="#cc0505", fg= "#ffff00")
            label1.place(relx=0.5, rely=0.15, anchor="center")
            label2 = Label(win, text="Invalid entry")
            label2.place(relx=0.5, rely=0.3, anchor='center')
            btn = Button(win, text="Back to Payment Function", command=win.destroy)
            btn.config(font=(FONT, 20, STYLE))
            btn.place(relx=0.5, rely=0.8, anchor='center')

            win.mainloop()




#slide 43
def confirmation_window():
    win = Tk()
    win.geometry("800x400")

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
        win.configure(bg = "#eb1e1e")

        error_label = Label(win, text = "ERROR: No such member", bg = "#eb1e1e")
        error_label.config(font=(FONT, 20, STYLE))
        error_label.place(relx=0.5, rely=0.15, anchor="center")
        
        back_button = Button(win, text = "Back to Payment Function", command = win.destroy)
        back_button.config(font=(FONT, 20, STYLE))
        back_button.place(relx=0.5, rely=0.8, anchor='center')

        win.mainloop()

    #no payment date or payment amount
    if not payment_date or not payment_amount:
        win.title("ERROR")
        win.configure(bg = "#eb1e1e")

        error_label = Label(win, text = "ERROR: Missing fields", bg = "#eb1e1e")
        error_label.config(font=(FONT, 20, STYLE))
        error_label.place(relx=0.5, rely=0.15, anchor="center")
        back_button = Button(win, text = "Back to Payment Function", command = win.destroy)
        back_button.config(font=(FONT, 20, STYLE))
        back_button.place(relx=0.5, rely=0.8, anchor='center')

        win.mainloop()

    #slide 35
    else:
        win.title("Confirmation of Payment Details")
        win.configure(bg = "#b0f556")

        titlelabel = Label(win, text="Please Confirm Details to be Correct", bg = "#b0f556", fg="black", width=30, height=2)
        titlelabel.config(font=(FONT, 20, STYLE))
        titlelabel.place(relx=0.5, rely=0.15, anchor="center")

        payment_due_label = Label(win, text = "Payment Due: ${}".format(payment_amount), bg = "#b0f556")
        payment_due_label.config(font=(FONT, 20, STYLE))
        payment_due_label.place(relx=0.30, rely=0.4, anchor='center')

        member_id_label = Label(win, text = "Member ID: {}".format(member_id), bg = "#b0f556")
        member_id_label.config(font=(FONT, 20, STYLE))
        member_id_label.place(relx=0.65, rely=0.4, anchor='center')

        payment_exact_label = Label(win, text = "Exact Fee Only", bg = "#b0f556")
        payment_exact_label.config(font=(FONT, 20, STYLE))
        payment_exact_label.place(relx=0.30, rely=0.6, anchor='center')

        payment_date_label = Label(win, text = "Payment Date: {}".format(payment_date), bg = "#b0f556")
        payment_date_label.config(font=(FONT, 20, STYLE))
        payment_date_label.place(relx=0.65, rely=0.6, anchor='center')

        confirm_button = Button(win, text = "Confirm Payment", command = lambda: [complete_payment(), win.destroy()])
        confirm_button.config(font=(FONT, 20, STYLE))
        confirm_button.place(relx=0.30, rely=0.8, anchor='center')

        back_button = Button(win, text = "Back to Payment Function", command = win.destroy)
        back_button.config(font=(FONT, 20, STYLE))
        back_button.place(relx=0.70, rely=0.8, anchor='center')

        win.mainloop()

#slide 42
def fine_details():
    win = Toplevel()
    win.title("Pay a Fine")
    win.geometry("1920x1080")

    image = Image.open("bg1.jpg")
    image = image.resize((1300, 650))

    bg = ImageTk.PhotoImage(image)
    canvas1 = Canvas(win, width = 1920, height = 1080)
    canvas1.pack(fill = "both", expand =  True)
    canvas1.create_image(0, 0, image = bg, anchor = "nw")

    #creating the fields + labels for slide 34
    global membership_id_field
    global payment_date_field
    global payment_amount_field

    instructions = Label(win, text='To Pay a Fine, Please Enter Information Below:', fg='black', bg='#c5e3e5', relief='raised', width=60, height=3)
    instructions.config(font=(FONT, FONT_SIZE, STYLE))
    instructions.place(relx=0.5, rely=0.09, anchor="center")

    membership_id_label = Label(win, text = "Membership ID")
    membership_id_label.config(font=(FONT, FONT_SIZE, STYLE))
    membership_id_label.place(relx=0.30, rely=0.35, anchor="center")
    membership_id_field = Entry(win, width = 60)
    membership_id_field.place(relx=0.60, rely=0.35, width = 660, height = 40, anchor="center")

    payment_date_label = Label(win, text = "Payment Date")
    payment_date_label.config(font=(FONT, FONT_SIZE, STYLE))
    payment_date_label.place(relx=0.30, rely=0.45, anchor="center")
    payment_date_field = Entry(win, width = 60)
    payment_date_field.place(relx=0.60, rely=0.45, width = 660, height = 40, anchor="center")

    payment_amount_label = Label(win, text = "Payment Amount")
    payment_amount_label.config(font=(FONT, FONT_SIZE, STYLE))
    payment_amount_label.place(relx=0.30, rely=0.55, anchor="center")
    payment_amount_field = Entry(win, width = 60)
    payment_amount_field.place(relx=0.60, rely=0.55, width = 660, height = 40, anchor="center")

    pay_button = Button(win, text='Pay Fine', padx=10, pady=10, command=confirmation_window, bg='#27c0ab', borderwidth=5, relief='raised')
    pay_button.config(font=(FONT,15,STYLE))
    pay_button.place(relx=0.35, rely=0.8, anchor='center')

    back_button = Button(win, text='Back to Fines Menu', padx=10, pady=10, command=win.destroy, bg='#27c0ab', borderwidth=5, relief='raised')
    back_button.config(font=(FONT,15,STYLE), wraplength=300)
    back_button.place(relx=0.65, rely=0.8, anchor='center')

    win.mainloop()
