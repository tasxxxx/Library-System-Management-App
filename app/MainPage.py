import tkinter as tk
import sqlalchemy as db
from MembersPage import *
from BooksMainPage import *
from LoansMainPage import *
from reservation_main import *
from fine_main import *
from ReportPage import *

USERNAME = "root"
PASSWORD = "mysqlUbae!!1"
HOST = "localhost"
PORT = 3306
DB = "Library"

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)

FONT = 'Arial'
FONT_SIZE = 25
STYLE = 'bold'

### bug: why does MembersPage pop up first? then after closing then MainMenu pops up?
### respective mainpages shouldnt run their function at the bottom
### slide 2
def mainMenu():

	win = tk.Tk()
	win.title("Main Menu")
	win.geometry("1920x1080")
	bg = ImageTk.PhotoImage(Image.open("C:/Users/user/Documents/GitHub/bt2102-assignment-1/resources/archi.jpg"))
	canvas1 = Canvas(win, width = 1920, height = 1080)
	canvas1.pack(fill = "both", expand =  True)
	canvas1.create_image(0, 0, image = bg, anchor = "nw")

	def navMainToMemb():
		membersMenu()
		win.destroy()

	def navMainToBooks():
		booksMenu()
		win.destroy()

	def navMainToLoans():
		loansMenu()
		win.destroy()

	def navMainToRes():
		reservation_main_menu()
		win.destroy()

	def navMainToFines():
		fine_main_menu()
		win.destroy()

	def navMainToReps():
		reportsMenu()
		win.destroy()

	title = tk.Label(win, text='(ALS)', fg='black', width=60, height=3)
	title.config(font=(FONT, FONT_SIZE, STYLE))
	title.place(relx=0.5, rely=0.09, anchor="center")

	btn_mem = tk.Button(win, text = "Membership", command = navMainToMemb)
	#btn_mem = tk.Button(win, text = "Membership", command = lambda: [membersMenu(), win.destroy()])
	#btn_mem = tk.Button(win, text = "Membership", command = membersMenu)
	btn_mem.config(font=(FONT, FONT_SIZE, STYLE))
	btn_mem.place(relx=0.3, rely=0.3, anchor="center")

	btn_books = tk.Button(win, text = "Books", command = navMainToBooks)
	#btn_books = tk.Button(win, text = "Books", command = booksMenu)
	btn_books.config(font=(FONT, FONT_SIZE, STYLE))
	btn_books.place(relx=0.5, rely=0.3, anchor="center")

	btn_loans = tk.Button(win, text = "Loans", command = navMainToLoans)
	btn_loans.config(font=(FONT, FONT_SIZE, STYLE))
	btn_loans.place(relx=0.7, rely=0.3, anchor="center")

	btn_res = tk.Button(win, text = "Reservations", command = navMainToRes)
	btn_res.config(font=(FONT, FONT_SIZE, STYLE))
	btn_res.place(relx=0.3, rely=0.6, anchor="center")

	btn_fines = tk.Button(win, text = "Fines", command = navMainToFines)
	btn_fines.config(font=(FONT, FONT_SIZE, STYLE))
	btn_fines.place(relx=0.5, rely=0.6, anchor="center")

	btn_reports = tk.Button(win, text = "Reports", command = navMainToReps)
	btn_reports.config(font=(FONT, FONT_SIZE, STYLE))
	btn_reports.place(relx=0.7, rely=0.6, anchor="center")

	win.mainloop()



mainMenu()