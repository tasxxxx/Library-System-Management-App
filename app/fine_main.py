from tkinter import *
from PIL import Image, ImageTk
from pay_fine import fine_details

#slide 41
def fine_main_menu():
    win = Tk()
    win.title("Fine")
    win.geometry("600x300")

    title_frame = LabelFrame(win, padx = 5, pady = 5)
    title_frame.grid(row = 0, column = 0, columnspan = 1, padx = 10, pady = 10)
    title_label = Label(title_frame, text = "Select one of the options below").pack()
    
    my_img = ImageTk.PhotoImage(Image.open("fines_photo.jpg").resize((200, 200), Image.ANTIALIAS))
    my_label = Label(image = my_img)
    my_label.grid(row = 1, column = 0)

    #creating the buttons
    reserve_button = Button(win, text = "Fine Payment", command = fine_details) #command for fine payment
    reserve_button.grid(row = 1, column = 3)

    back_button = Button(win, text = "Back to Main Menu", command = win.destroy)
    back_button.grid(row = 1, column = 4)

    win.mainloop()

