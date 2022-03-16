import sqlalchemy as db
import tkinter as tk
from datetime import *
from sqlalchemy.exc import IntegrityError, DataError, OperationalError

FONT = 'Arial'
FONT_SIZE = 25
SMALL_FONT_SIZE = 10
STYLE = 'bold'

USERNAME = "root"
PASSWORD = "" ## enter password
HOST = "localhost"
PORT = 3306
DB = "Library"

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
cursor = engine.connect()

## slide 13
def update():

	global ent_memId
	global memberInfo
	global memId
	global ent_name
	global ent_faculty
	global ent_phoneNo
	global ent_email
	global slide13

	# fetch memId rows from MEMBERS to see if this member exists
	sql3 = "SELECT * FROM Members WHERE memberId = '{}'".format(memId)
	memberInfo = cursor.execute(sql3).fetchall()

	# query from Members
	# name = memberInfo[0][1]
	# faculty = memberInfo[0][2]
	# phoneNo = memberInfo[0][3]
	# email = memberInfo[0][4]

	newname = ent_name.get()
	newfaculty = ent_faculty.get()
	newphoneno = ent_phoneNo.get()
	newemail = ent_email.get()

	slide13 = tk.Tk()
	slide13.geometry("800x400")
	slide13.configure(bg = "#b0f556")

	## check if fields are empty? sequence of the checking, alr check below


	info = "Member ID: {}\nName: {}\nFaculty: {}\nPhone Number: {}\nEmail Address: {}".format(memId, newname, newfaculty, newphoneno, newemail)

	bodylabel = tk.Label(slide13, text=info, bg = "#b0f556", fg="#000000", width=30, height=12)
	bodylabel.config(font=(FONT, 15, STYLE))
	bodylabel.place(relx=0.5, rely=0.50, anchor="center")

	titlelabel = tk.Label(slide13, text="Please Confirm Updated Details to be Correct", fg="black", bg = "#b0f556")
	titlelabel.config(font=(FONT, 20, STYLE))
	titlelabel.place(relx=0.5, rely=0.2, anchor="center")

	confirm_delete_btn = tk.Button(slide13, text='Confirm Update', padx=10, pady=10, command=lambda:confirmUpdate(memId, newname , newfaculty, newphoneno, newemail), bg='#27c0ab', borderwidth=5, relief='raised')
	confirm_delete_btn.config(font=(FONT,15,STYLE))
	confirm_delete_btn.place(relx=0.3, rely=0.8, anchor='center')

	back_to_update_btn = tk.Button(slide13, text='Back to Update Function', padx=10, pady=10, command=slide13.destroy, bg='#27c0ab', borderwidth=5, relief='raised')
	back_to_update_btn.config(font=(FONT,15,STYLE), wraplength=300)
	back_to_update_btn.place(relx=0.7, rely=0.8, anchor='center')

	slide13.mainloop()



## slide 12, done
def updateMember():

	global ent_memId
	global memberInfo
	global memId
	global ent_name
	global ent_faculty
	global ent_phoneNo
	global ent_email
	global slide12

	slide12 = tk.Tk()
	

	memId = ent_memId.get()

	# fetch memId rows from MEMBERS to see if this member exists
	sql3 = "SELECT * FROM Members WHERE memberId = '{}'".format(memId)
	memberInfo = cursor.execute(sql3).fetchall()

	if len(memberInfo) == 0:
		slide12.geometry("800x400")
		slide12.configure(bg = "#eb1e1e")

		label1 = tk.Label(slide12, text='Error: No such member found', fg='black', bg = "#eb1e1e", width=60, height=3)
		label1.config(font=(FONT, 20, STYLE))
		label1.place(relx=0.5, rely=0.15, anchor="center")

		btn_back = tk.Button(slide12, text = "Back", command = slide12.destroy)
		btn_back.config(font=(FONT, 20, STYLE))
		btn_back.place(relx=0.5, rely=0.8, anchor='center')

		slide12.mainloop()

	## slide 12
	else:

		slide12.geometry("1920x1080")

		instructions = tk.Label(slide12, text='Please Enter Requested Information Below:', fg='black', bg='#c5e3e5', relief='raised', width=60, height=3)
		instructions.config(font=(FONT, FONT_SIZE, STYLE))
		instructions.place(relx=0.5, rely=0.09, anchor="center")

		lbl_headermemId = tk.Label(slide12, text = "Membership ID", fg='black')
		lbl_headermemId.config(font=(FONT, FONT_SIZE, STYLE))
		lbl_headermemId.place(relx=0.35, rely=0.25, anchor="center")
		lbl_memId = tk.Label(slide12, text = memId)
		lbl_memId.config(font=(FONT, FONT_SIZE, STYLE))
		lbl_memId.place(relx=0.65, rely=0.25, width = 660, height = 40, anchor="center")

		lbl_name = tk.Label(slide12, text = "Name")
		lbl_name.config(font=(FONT, FONT_SIZE, STYLE))
		lbl_name.place(relx=0.35, rely=0.35, anchor="center")
		ent_name = tk.Entry(slide12, width = 60)
		ent_name.place(relx=0.65, rely=0.35, width = 660, height = 40, anchor="center")

		lbl_faculty = tk.Label(slide12, text = "Faculty")
		lbl_faculty.config(font=(FONT, FONT_SIZE, STYLE))
		lbl_faculty.place(relx=0.35, rely=0.45, anchor="center")
		ent_faculty = tk.Entry(slide12, width = 60)
		ent_faculty.place(relx=0.65, rely=0.45, width = 660, height = 40, anchor="center")

		lbl_phoneNo = tk.Label(slide12, text = "Phone Number")
		lbl_phoneNo.config(font=(FONT, FONT_SIZE, STYLE))
		lbl_phoneNo.place(relx=0.35, rely=0.55, anchor="center")
		ent_phoneNo = tk.Entry(slide12, width = 60)
		ent_phoneNo.place(relx=0.65, rely=0.55, width = 660, height = 40, anchor="center")

		lbl_email = tk.Label(slide12, text = "Email Address")
		lbl_email.config(font=(FONT, FONT_SIZE, STYLE))
		lbl_email.place(relx=0.35, rely=0.65, anchor="center")
		ent_email = tk.Entry(slide12, width = 60)
		ent_email.place(relx=0.65, rely=0.65, width = 660, height = 40, anchor="center")

		btn_updateMember = tk.Button(slide12, text = "Update Member", command = update)
		btn_updateMember.config(font=(FONT, 15, STYLE))
		btn_updateMember.place(relx=0.3, rely=0.8, anchor="center")

		btn_backMembMenu = tk.Button(slide12, text = "Back to Membership Menu", command = slide12.destroy)
		btn_backMembMenu.config(font=(FONT, 15, STYLE))
		btn_backMembMenu.place(relx=0.7, rely=0.8, anchor="center")

		slide12.mainloop()



### button in slide 13 to go slide 14, 15
def confirmUpdate(memberId, name, faculty, phoneNo, email):

	def navToUpdateMember():
		slide1415.destroy()
		slide13.destroy()
		slide12.destroy()

	slide1415 = tk.Tk()
	slide1415.geometry("800x400")

	## slide 15
	# check if fields are missing or incomplete
	if name == "" or faculty == "" or phoneNo == "" or email == "":

		slide1415.configure(bg = "#eb1e1e")

		label1 = tk.Label(slide1415, text="Error!", bg="#cc0505", fg= "#ffff00")
		label1.config(font=(FONT, 20, STYLE))
		label1.place(relx=0.5, rely=0.15, anchor="center")

		label2 = tk.Label(slide1415, text="Missing or Incomplete fields.")
		label2.config(font=(FONT, 20, STYLE))
		label2.place(relx=0.5, rely=0.3, anchor="center")

		btn = tk.Button(slide1415, text="Back to Update Function", command= lambda: [slide1415.destroy(), slide13.destroy(), slide12.destroy()])
		btn.config(font=(FONT, 20, STYLE))
		btn.place(relx=0.5, rely=0.8, anchor='center')


	## slide 14
	else:

		try:

			slide1415.configure(bg = "#b0f556")

			update_member = """UPDATE Members SET memberName='{}', faculty='{}', phone={}, email='{}' WHERE memberId='{}';""".format(name,\
			faculty, phoneNo, email, memberId)
			cursor.execute(update_member)

			label1 = tk.Label(slide1415, text="Success!", bg = "#b0f556")
			label1.config(font=(FONT, 20, STYLE))
			label1.place(relx=0.5, rely=0.15, anchor="center")

			label2 = tk.Label(slide1415, text="ALS Membership Updated.", bg = "#b0f556")
			label2.config(font=(FONT, 20, STYLE))
			label2.place(relx=0.5, rely=0.3, anchor="center")

			btn1 = tk.Button(slide1415, text="Create Another Member", command=lambda: [slide1415.destroy(), slide13.destroy(), slide12.destroy(), updateMembMenu.destroy()])
			btn1.config(font=(FONT, 15, STYLE))
			btn1.place(relx=0.3, rely=0.8, anchor="center")

			btn2 = tk.Button(slide1415, text="Back to Update Function", command=lambda: [slide1415.destroy(), slide13.destroy(), slide12.destroy()])
			btn2.config(font=(FONT, 15, STYLE))
			btn2.place(relx=0.7, rely=0.8, anchor="center")

			slide1415.mainloop()


		except (IntegrityError, ValueError, OperationalError):

			slide1415.configure(bg = "#eb1e1e")

			label1 = tk.Label(slide1415, text="Error!", bg="#cc0505", fg= "#ffff00")
			label1.config(font=(FONT, 20, STYLE))
			label1.place(relx=0.5, rely=0.15, anchor="center")

			label2 = tk.Label(slide1415, text="Invalid entry")
			label2.config(font=(FONT, 20, STYLE))
			label2.place(relx=0.5, rely=0.3, anchor="center")

			btn = tk.Button(slide1415, text="Back to Update Function", command=lambda: [slide1415.destroy(), slide13.destroy(), slide12.destroy()])
			btn.config(font=(FONT, 20, STYLE))
			btn.place(relx=0.5, rely=0.8, anchor='center')

			slide1415.mainloop()


### slide 11
def updateMembersMenu():

	global updateMembMenu
	global ent_memId

	updateMembMenu = tk.Tk()
	updateMembMenu.title("Update Membership")
	updateMembMenu.geometry("1920x1080")


	instructions = tk.Label(updateMembMenu, text='To Update Member, Please Enter Membership ID:', fg='black', bg='#c5e3e5', relief='raised', width=60, height=3)
	instructions.config(font=(FONT, FONT_SIZE, STYLE))
	instructions.place(relx=0.5, rely=0.09, anchor="center")

	lbl_memId = tk.Label(updateMembMenu, text = "Membership ID")
	lbl_memId.config(font=(FONT, FONT_SIZE, STYLE))
	lbl_memId.place(relx=0.35, rely=0.5, anchor="center")
	ent_memId = tk.Entry(updateMembMenu, width = 60)
	ent_memId.place(relx=0.65, rely=0.5, width = 660, height = 40, anchor="center")

	btn_updateMember = tk.Button(updateMembMenu, text = "Update Member", command = updateMember)
	btn_updateMember.config(font=(FONT, 15, STYLE))
	btn_updateMember.place(relx=0.3, rely=0.8, anchor="center")

	btn_backMembMenu = tk.Button(updateMembMenu, text = "Back to Membership Menu", command = updateMembMenu.destroy)
	btn_backMembMenu.config(font=(FONT, 15, STYLE))
	btn_backMembMenu.place(relx=0.7, rely=0.8, anchor="center")

	updateMembMenu.mainloop()

