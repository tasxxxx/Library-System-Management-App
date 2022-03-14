import sqlalchemy as db
from tkinter import *
import LoansBorrow
import LoansReturn
from PIL import ImageTk, Image

USERNAME = "root"
PASSWORD = "Crunchyapples99"
HOST = "localhost"
PORT = 3306
DB = "Library"

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
cursor = engine.connect()

def loansMenu():

	root = Tk()

	TITLE_FONT = ("Gill Sans MT", 15)
	DEFAULT_FONT = ("Gill Sans MT", 11)

	root.title("Loans")
	root.configure(bg = "white")

	book_img = ImageTk.PhotoImage(Image.open("C:/Users/Brexton/Desktop/Y2S2/BT2102/Assignment 1/loans.jpg"))
	book_label = Label(image = book_img, width = 300, height = 200)
	book_label.grid(row = 2, column = 0, rowspan = 2)

	toplabel = Label(root, text = "Select one of the Options below:", font = TITLE_FONT, bg = "#5AA9E6")
	toplabel.grid(row = 1, column = 0, columnspan = 2)

	label1 = Button(root, text = "6. Borrow", font = DEFAULT_FONT, bg = "#7FC8F8", command = LoansBorrow.loansBorrow)
	label1.grid(row = 2, column = 1)
	label2 = Label(root, text = "Book Borrowing", font = DEFAULT_FONT, bg = "white")
	label2.grid(row = 2, column = 2, sticky = W)
	label3 = Button(root, text = "7. Return", font = DEFAULT_FONT, bg = "#7FC8F8", command = LoansReturn.loansReturn)
	label3.grid(row = 3, column = 1)
	label4 = Label(root, text = "Book Returning", font = DEFAULT_FONT, bg = "white")
	label4.grid(row = 3, column = 2, sticky = W)

	btn = Button(root, text = "Back To Main Menu", font = DEFAULT_FONT, bg = "#5AA9E6", command = root.destroy)
	btn.grid(row = 4, column = 0, columnspan = 2)

	root.mainloop()