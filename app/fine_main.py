from tkinter import *
from PIL import Image, ImageTk
from pay_fine import fine_details

FONT = 'Arial'
FONT_SIZE = 25
SMALL_FONT_SIZE = 10
STYLE = 'bold'

#slide 41
def fine_main_menu():
    win = Toplevel()
    win.title("Fine")
    win.geometry("1920x1080")

    image = Image.open("bg1.jpg")
    image = image.resize((1300, 650))

    bg = ImageTk.PhotoImage(image)
    canvas1 = Canvas(win, width = 1920, height = 1080)
    canvas1.pack(fill = "both", expand =  True)
    canvas1.create_image(0, 0, image = bg, anchor = "nw")

    # title_frame = LabelFrame(win, padx = 5, pady = 5)
    # title_frame.grid(row = 0, column = 0, columnspan = 1, padx = 10, pady = 10)
    # title_label = Label(title_frame, text = "Select one of the options below").pack()

    instructions = Label(win, text='Select one of the Options below:', fg='black', bg='#c5e3e5', relief='raised', width=60, height=3)
    instructions.config(font=(FONT, FONT_SIZE, STYLE))
    instructions.place(relx=0.5, rely=0.09, anchor="center")

    # Creating Image
    img = Image.open("fines_photo.jpg")
    img = img.resize((200, 200), Image.ANTIALIAS)
    my_img = ImageTk.PhotoImage(img)

    # Putting Image on the window instead of menu page
    img_canvas = Canvas(win, width=400, height=300)
    img_canvas.place(relx=0.2, rely=0.50, anchor="w")
    img_canvas.create_image(10, 10, anchor="nw", image=my_img)

    #creating the buttons
    reserve_button = Button(win, text = "10. Payment", command = fine_details) #command for fine payment
    reserve_button.config(font=(FONT, FONT_SIZE, STYLE))
    reserve_button.place(relx=0.45, rely=0.45, anchor="center")

    desc = Label(win, text='Fine Payment', fg='black')
    desc.config(font=(FONT, FONT_SIZE, STYLE))
    desc.place(relx=0.65, rely=0.45, anchor="center")

    btn_home = Button(win, text='Back to Main Menu', bg='#c5e3e5', relief='raised', width=60, height=1, command = win.destroy)
    btn_home.config(font=(FONT, FONT_SIZE, STYLE))
    btn_home.place(relx=0.5, rely=0.80, anchor="center")

    win.mainloop()

