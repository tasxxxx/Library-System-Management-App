import sqlalchemy as db
from tkinter import *
import LoansBorrow
import LoansReturn
from PIL import ImageTk, Image

USERNAME = "root"
PASSWORD = "Hoepeng.0099"
HOST = "localhost"
PORT = 3306
DB = "Library"

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
cursor = engine.connect()

FONT = 'Arial'
FONT_SIZE = 25
SMALL_FONT_SIZE = 10
STYLE = 'bold'

def loansMenu():

	root = Toplevel()
	root.geometry("1920x1080")

	root.title("Loans")
	root.configure(bg = "white")

	# Inserting an IMAGE on the left side of the page
	global my_img
	image = Image.open("loans.jpg")
	image = image.resize((500, 400), Image.ANTIALIAS)
	my_img = ImageTk.PhotoImage(image)
	img_canvas = Canvas(root, width=300, height=250)
	img_canvas.place(relx=0.1, rely=0.50, anchor="w")
	img_canvas.create_image(10, 10, anchor="w", image=my_img)

	# old code
	# book_img = ImageTk.PhotoImage(Image.open("loans.jpg"))
	# book_label = Label(image = book_img, width = 300, height = 200)
	# book_label.grid(row = 2, column = 0, rowspan = 2)

	toplabel = Label(root, text = "Select one of the Options below:",  fg='black', bg='#c5e3e5', relief='raised', width=60, height=3)
	toplabel.config(font=(FONT, FONT_SIZE, STYLE))
	toplabel.place(relx=0.5, rely=0.09, anchor="center")

	label1 = Button(root, text = "6. Borrow", command = LoansBorrow.loansBorrow)
	label1.config(font=(FONT, FONT_SIZE, STYLE))
	label1.place(relx=0.4, rely=0.3, anchor="center")

	label2 = Label(root, text = "Book Borrowing", fg = "black")
	label2.config(font=(FONT, FONT_SIZE, STYLE))
	label2.place(relx=0.6, rely=0.3, anchor="center")

	label3 = Button(root, text = "7. Return", command = LoansReturn.loansReturn)
	label3.config(font=(FONT, FONT_SIZE, STYLE))
	label3.place(relx=0.4, rely=0.45, anchor="center")

	label4 = Label(root, text = "Book Returning", fg = 'black')
	label4.config(font=(FONT, FONT_SIZE, STYLE))
	label4.place(relx=0.6, rely=0.45, anchor="center")

	btn = Button(root, text = "Back To Main Menu", bg='#c5e3e5', relief='raised', width=60, height=1, command = root.destroy)
	btn.config(font=(FONT, FONT_SIZE, STYLE))
	btn.place(relx=0.5, rely=0.80, anchor="center")

	root.mainloop()