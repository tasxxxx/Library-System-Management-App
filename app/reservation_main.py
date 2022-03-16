from tkinter import *
from PIL import Image, ImageTk
from make_reservation import reservation_details
from cancel_reservation import cancel_reservation_details

FONT = 'Arial'
FONT_SIZE = 25
SMALL_FONT_SIZE = 10
STYLE = 'bold'

#slide 33
def reservation_main_menu():
    win =  Toplevel()
    win.title("Reservations")
    win.geometry("600x300")

	image = Image.open("bg1.jpg")
	image = image.resize((1300, 650))

	bg = ImageTk.PhotoImage(image)
	canvas1 = Canvas(win, width = 1920, height = 1080)
	canvas1.pack(fill = "both", expand =  True)
	canvas1.create_image(0, 0, image = bg, anchor = "nw")

    label = tk.Label(root, text="Select one of the Options below", fg='black', bg='#c5e3e5', relief='raised', width=60,
                     height=3)
    label.config(font=(FONT, FONT_SIZE, STYLE))
    label.place(relx=0.5, rely=0.09, anchor="center")

    image = Image.open("reservations_photo.jpg")
    image = image.resize((400, 300), Image.ANTIALIAS)
    my_img = ImageTk.PhotoImage(image)
    img_canvas = tk.Canvas(root, width=300, height=250)
    img_canvas.place(relx=0.2, rely=0.50, anchor="w")
    img_canvas.create_image(50, 50, anchor="w", image=my_img)


    #creating the buttons
    reserve_button = Button(win, text = "Book Reservation", command = reservation_details)
	btn_create.config(font=(FONT, FONT_SIZE, STYLE))
	btn_create.place(relx=0.6, rely=0.3, anchor="center")

    cancel_button = Button(win, text = "Cancel Reservation", command = cancel_reservation_details)
    cancel_button.config(font=(FONT, FONT_SIZE, STYLE))
	cancel_button.place(relx=0.6, rely=0.45, anchor="center")

    back_button = Button(win, text = "Back to Main Menu", command = win.destroy)
    back_button.config(font=(FONT, FONT_SIZE, STYLE))
	back_button.place(relx=0.5, rely=0.80, anchor="center")
    
    win.mainloop()
