from turtle import bgcolor
import sqlalchemy as db
from tkinter import *
import BooksAcquisition
import BooksWithdrawal
from PIL import ImageTk, Image

USERNAME = "root"
PASSWORD = "mysqlUbae!!1"
HOST = "localhost"
PORT = 3306
DB = "Library"

FONT = 'Arial'
FONT_SIZE = 25
STYLE = 'bold'

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
cursor = engine.connect()

def booksMenu():

	root = Tk()
	#root = Toplevel(win)

	root.title("Books")
	root.geometry("1920x1080")
	root.configure(bg = "white")

	picture = Image.open("C:/Users/user/Documents/GitHub/bt2102-assignment-1/resources/books.jpg")
	book_img = ImageTk.PhotoImage(image=picture)
	##book_img = ImageTk.PhotoImage(Image.open("C:/Users/Brexton/Desktop/Y2S2/BT2102/Assignment 1/books.jpg"))
	book_label = Label(image = book_img, width = 300, height = 200)
	book_label.place(relx=0.4, rely=0.45, anchor="center")

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