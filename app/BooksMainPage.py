from turtle import bgcolor
import sqlalchemy as db
from tkinter import *
import BooksAcquisition
import BooksWithdrawal
from PIL import ImageTk, Image

USERNAME = "root"
PASSWORD = "Dcmmq9ck5s24!"
HOST = "localhost"
PORT = 3306
DB = "Library"

FONT = 'Arial'
FONT_SIZE = 25
STYLE = 'bold'

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
cursor = engine.connect()

def booksMenu():

	root = Toplevel()

	root.title("Books")
	root.geometry("1920x1080")
	root.configure(bg = "white")

	image = Image.open("bg1.jpg")
	image = image.resize((1300, 650))

	bg = ImageTk.PhotoImage(image)
	canvas1 = Canvas(root, width = 1920, height = 1080)
	canvas1.pack(fill = "both", expand =  True)
	canvas1.create_image(0, 0, image = bg, anchor = "nw")

	# Inserting an IMAGE on the left side of the page
	global my_img
	image = Image.open("books.jpg")
	image = image.resize((500, 400), Image.ANTIALIAS)
	my_img = ImageTk.PhotoImage(image)
	img_canvas = Canvas(root, width=300, height=250)
	img_canvas.place(relx=0.05, rely=0.4, anchor="w")
	img_canvas.create_image(10, 10, anchor="w", image=my_img)

	toplabel = Label(root, text = "Select one of the Options below:", fg='black', bg='#c5e3e5', relief='raised', width=60, height=3)
	toplabel.config(font=(FONT, FONT_SIZE, STYLE))
	toplabel.place(relx=0.5, rely=0.09, anchor="center")

	label1 = Button(root, text = "4. Acquisition", bg = "#7fc8f8", command = BooksAcquisition.booksAcquisition)
	label1.config(font=(FONT, FONT_SIZE, STYLE))
	label1.place(relx=0.4, rely=0.3, anchor="center")
	label2 = Label(root, text = "Book Acquisition", bg = "white")
	label2.config(font=(FONT, FONT_SIZE, STYLE))
	label2.place(relx=0.6, rely=0.3, anchor="center")
	label3 = Button(root, text = "5. Withdrawal", bg = "#7fc8f8", command = BooksWithdrawal.booksWithdrawal)
	label3.config(font=(FONT, FONT_SIZE, STYLE))
	label3.place(relx=0.4, rely=0.4, anchor="center")
	label4 = Label(root, text = "Book Withdrawal", bg = "white")
	label4.config(font=(FONT, FONT_SIZE, STYLE))
	label4.place(relx=0.6, rely=0.4, anchor="center")

	btn = Button(root, text = "Back To Main Menu", bg = "#5AA9E6", command = root.destroy)
	btn.config(font=(FONT, FONT_SIZE, STYLE))
	btn.place(relx=0.5, rely=0.8, anchor="center")

	root.mainloop()
