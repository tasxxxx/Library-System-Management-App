import sqlalchemy as db
import tkinter as tk
from datetime import *
from sqlalchemy.exc import IntegrityError, DataError, OperationalError
from PIL import ImageTk, Image

FONT = 'Arial'
FONT_SIZE = 25
SMALL_FONT_SIZE = 10
STYLE = 'bold'

USERNAME = "root"
PASSWORD = "Dcmmq9ck5s24!" ## insert password
HOST = "localhost"
PORT = 3306
DB = "Library"

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
cursor = engine.connect()


def createMember():

	win = tk.Toplevel()
	win.geometry("1920x1080")

	image = Image.open("bg1.jpg")
	image = image.resize((1300, 650))

	bg = ImageTk.PhotoImage(image)
	canvas1 = tk.Canvas(win, width = 1920, height = 1080)
	canvas1.pack(fill = "both", expand =  True)
	canvas1.create_image(0, 0, image = bg, anchor = "nw")

	global ent_memId
	global ent_name
	global ent_faculty
	global ent_phoneNo
	global ent_email

	#store the input into variables
	memId = ent_memId.get()
	name = ent_name.get()
	faculty = ent_faculty.get()
	phoneNo = ent_phoneNo.get()
	email = ent_email.get()

	# fetch memId rows from MEMBERS
	check_membership_id = "SELECT * FROM Members WHERE memberId = '{}'".format(memId)
	valid_membership_id = cursor.execute(check_membership_id).fetchall()

	## popup logic not working properly, to fix: member already exists error
	## slide 7
	# check if fields are missing or incomplete, or member already exists
	if memId == "" or name == "" or faculty == "" or phoneNo == "" or email == "" or valid_membership_id:
		label1 = tk.Label(win, text="Error!", bg="#cc0505", fg= "#ffff00")
		label1.pack()
		label2 = tk.Label(win, text="Member already exists; Missing or Incomplete fields.")
		label2.pack()
		btn = tk.Button(win, text="Back to Create Function", command=win.destroy)
		btn.pack()

		win.mainloop()

	## slide 6
	else:

		try:
			insert_member = "INSERT INTO Members VALUES ('{}', '{}', '{}', '{}', '{}')".format(memId, name, faculty, phoneNo, email)
			cursor.execute(insert_member)

			label1 = tk.Label(win, text="Success!")
			label1.pack()
			label2 = tk.Label(win, text="ALS Membership created.")
			label2.pack()
			btn = tk.Button(win, text="Back to Create Function", command=win.destroy)
			btn.pack()

			win.mainloop()

		except (IntegrityError, ValueError, OperationalError):
			label1 = tk.Label(win, text="Error!", bg="#cc0505", fg= "#ffff00")
			label1.pack()
			label2 = tk.Label(win, text="Invalid entry")
			label2.pack()
			btn = tk.Button(win, text="Back to Create Function", command=win.destroy)
			btn.pack()

			win.mainloop()

## slide 5
def createMembersMenu():

	global createMembMenu
	global ent_memId
	global ent_name
	global ent_faculty
	global ent_phoneNo
	global ent_email

	createMembMenu = tk.Toplevel()
	createMembMenu.title("Create Membership")
	createMembMenu.geometry("1920x1080")

	image = Image.open("bg1.jpg")
	image = image.resize((1300, 650))

	bg = ImageTk.PhotoImage(image)
	canvas1 = tk.Canvas(createMembMenu, width = 1920, height = 1080)
	canvas1.pack(fill = "both", expand =  True)
	canvas1.create_image(0, 0, image = bg, anchor = "nw")

	def navToMain():
		mainMenu()
		createMembMenu.destroy()

	instructions = tk.Label(createMembMenu, text='To Create Member, Please Enter Requested Information Below:', fg='black', bg='#c5e3e5', relief='raised', width=60, height=3)
	instructions.config(font=(FONT, FONT_SIZE, STYLE))
	instructions.place(relx=0.5, rely=0.09, anchor="center")

	lbl_memId = tk.Label(createMembMenu, text = "Membership ID")
	lbl_memId.config(font=(FONT, FONT_SIZE, STYLE))
	lbl_memId.place(relx=0.35, rely=0.25, anchor="center")
	ent_memId = tk.Entry(createMembMenu, width = 60)
	ent_memId.place(relx=0.65, rely=0.25, width = 660, height = 40, anchor="center")

	lbl_name = tk.Label(createMembMenu, text = "Name")
	lbl_name.config(font=(FONT, FONT_SIZE, STYLE))
	lbl_name.place(relx=0.35, rely=0.35, anchor="center")
	ent_name = tk.Entry(createMembMenu, width = 60)
	ent_name.place(relx=0.65, rely=0.35, width = 660, height = 40, anchor="center")

	lbl_faculty = tk.Label(createMembMenu, text = "Faculty")
	lbl_faculty.config(font=(FONT, FONT_SIZE, STYLE))
	lbl_faculty.place(relx=0.35, rely=0.45, anchor="center")
	ent_faculty = tk.Entry(createMembMenu, width = 60)
	ent_faculty.place(relx=0.65, rely=0.45, width = 660, height = 40, anchor="center")

	lbl_phoneNo = tk.Label(createMembMenu, text = "Phone Number")
	lbl_phoneNo.config(font=(FONT, FONT_SIZE, STYLE))
	lbl_phoneNo.place(relx=0.35, rely=0.55, anchor="center")
	ent_phoneNo = tk.Entry(createMembMenu, width = 60)
	ent_phoneNo.place(relx=0.65, rely=0.55, width = 660, height = 40, anchor="center")

	lbl_email = tk.Label(createMembMenu, text = "Email Address")
	lbl_email.config(font=(FONT, FONT_SIZE, STYLE))
	lbl_email.place(relx=0.35, rely=0.65, anchor="center")
	ent_email = tk.Entry(createMembMenu, width = 60)
	ent_email.place(relx=0.65, rely=0.65, width = 660, height = 40, anchor="center")

	btn_createMember = tk.Button(createMembMenu, text = "Create Member", command = createMember)
	btn_createMember.config(font=(FONT, FONT_SIZE, STYLE))
	btn_createMember.place(relx=0.3, rely=0.8, anchor="center")

	btn_backMainMenu = tk.Button(createMembMenu, text = "Back to Main Menu", command = lambda: [createMembMenu.destroy(), win.destroy()])
	btn_backMainMenu.config(font=(FONT, FONT_SIZE, STYLE))
	btn_backMainMenu.place(relx=0.7, rely=0.8, anchor="center")

	createMembMenu.mainloop()

