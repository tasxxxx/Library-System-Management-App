from turtle import bgcolor
import sqlalchemy as db
from tkinter import *
import BooksAcquisition
import BooksWithdrawal
from PIL import ImageTk, Image

USERNAME = "root"
PASSWORD = "Hoepeng.0099"
HOST = "localhost"
PORT = 3306
DB = "Library"

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
cursor = engine.connect()

def booksMenu():

	root = Tk()
	#root = Toplevel(win)

	TITLE_FONT = ("Gill Sans MT", 15)
	DEFAULT_FONT = ("Gill Sans MT", 11)

	root.title("Books")
	root.configure(bg = "white")

	picture = Image.open("books.jpg")
	book_img = ImageTk.PhotoImage(image=picture)
	##book_img = ImageTk.PhotoImage(Image.open("C:/Users/Brexton/Desktop/Y2S2/BT2102/Assignment 1/books.jpg"))
	book_label = Label(image = book_img, width = 300, height = 200)
	book_label.grid(row = 2, column = 0, rowspan = 2)

	toplabel = Label(root, text = "Select one of the Options below:", font = TITLE_FONT, bg = "#5AA9E6")
	toplabel.grid(row = 1, column = 0, columnspan = 4)

	label1 = Button(root, text = "4. Acquisition", font = DEFAULT_FONT, bg = "#7fc8f8", command = BooksAcquisition.booksAcquisition)
	label1.grid(row = 2, column = 2)
	label2 = Label(root, text = "Book Acquisition", font = DEFAULT_FONT, bg = "white")
	label2.grid(row = 2, column = 3)
	label3 = Button(root, text = "5. Withdrawal", font = DEFAULT_FONT, bg = "#7fc8f8", command = BooksWithdrawal.booksWithdrawal)
	label3.grid(row = 3, column = 2)
	label4 = Label(root, text = "Book Withdrawal", font = DEFAULT_FONT, bg = "white")
	label4.grid(row = 3, column = 3)

	btn = Button(root, text = "Back To Main Menu", font = DEFAULT_FONT, bg = "#5AA9E6", command = root.destroy)
	btn.grid(row = 4, column = 0, columnspan = 4)

	root.mainloop()