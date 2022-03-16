import sqlalchemy as db
import tkinter as tk
from datetime import *

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


def delete(idinput):
	delete_member = "DELETE FROM Members WHERE memberId = '{}'".format(idinput)
	cursor.execute(delete_member)

	deletepopup = tk.Tk()
	deletepopup.geometry("800x400")
	deletepopup.configure(bg = "#b0f556")

	label1 = tk.Label(deletepopup, text='Membership deleted', fg='black', bg='#c5e3e5', relief='raised', width=60, height=3)
	label1.config(font=(FONT, FONT_SIZE, STYLE))
	label1.place(relx=0.5, rely=0.15, anchor="center")

	btn_back = tk.Button(deletepopup, text = "Back", command = lambda: [deletepopup.destroy(), win.destroy()])
	btn_back.config(font=(FONT, FONT_SIZE, STYLE))
	btn_back.place(relx=0.5, rely=0.8, anchor="center")

	
	deletepopup.mainloop()


## slide 9
# confirmation popup and error 
def deleteMember():
	#store the input into variable
	memId = ent_memId.get()

	# fetch memId rows from MEMBERS
	sql2 = "SELECT * FROM Members WHERE memberId = '{}'".format(memId)
	memberInfo = cursor.execute(sql2).fetchall()

	win = tk.Tk()
	win.geometry("800x400")

	if len(memberInfo) == 0:

		win.configure(bg = "#b0f556")

		label1 = tk.Label(win, text='Error: No such member found', fg='black', bg="#b0f556", relief='raised', width=60, height=3)
		label1.config(font=(FONT, FONT_SIZE, STYLE))
		label1.place(relx=0.5, rely=0.15, anchor="center")

		btn_back = tk.Button(win, text = "Back", command = win.destroy)
		label1.config(font=(FONT, FONT_SIZE, STYLE))
		btn_back.place(relx=0.5, rely=0.8, anchor="center")

		win.mainloop()


	# query from Members
	name = memberInfo[0][1]
	faculty = memberInfo[0][2]
	phoneNo = memberInfo[0][3]
	email = memberInfo[0][4]

	# TODO: check BORROW WHERE memberId, all books are already returned: returnDate != null
	sqlcheck_on_loan = "SELECT * FROM Borrow WHERE borrowMemberId = '{}'".format(memId)
	loan_records = cursor.execute(sqlcheck_on_loan).fetchall()
	on_loan = False
	for record in loan_records:
		return_date = record[3]
		if return_date is None:
			on_loan = True

	# DONE check FINES WHERE memberId, all fines are already paid: no records should exist
	sqlcheck_gotfines = "SELECT * FROM Fine WHERE memberId = '{}'".format(memId)
	got_fines = cursor.execute(sqlcheck_gotfines).fetchall()


	# dont need check for reservations? on member delete, reservation cascade?
	# sqlcheck_gotreservations = "SELECT * FROM Reservation WHERE memberId = '{}'".format(memId)
	# reservation_records = cursor.execute(sqlcheck_gotreservations).fetchall()
	# got_reservations = False
	# if reservation_records:
	# 	got_reservation = True


	##### TODO, font not standardised also
	# fail: TODO check loans, reservations and fines
	# if got_fines or on_loan or got_reservation:
	if got_fines or on_loan:

		win.configure(bg = "#eb1e1e")

		label1 = tk.Label(win, text="Error!", bg="#eb1e1e", fg= "#ffff00")
		label1.config(font=(FONT, FONT_SIZE, STYLE))
		label1.place(relx=0.5, rely=0.15, anchor="center")

		label2 = tk.Label(win, text="Member has loans, reservations or outstanding fines.", bg = "#eb1e1e")
		label2.config(font=(FONT, FONT_SIZE, STYLE))
		label2.place(relx=0.5, rely=0.3, anchor="center")


		btn = tk.Button(win, text="Back to Delete Function", command=win.destroy)
		btn.config(font=(FONT, 20, STYLE))
		btn.place(relx=0.5, rely=0.8, anchor='center')

	# success, deletion SQL, reservations cascade in SQL
	else:

		win.configure(bg = "#b0f556")

		memberInfo = "Member ID: {}\nName: {}\nFaculty: {}\nPhone Number: {}\nEmail Address: {}".format(memId, name, faculty, phoneNo, email)

		bodylabel = tk.Label(win, text=memberInfo, bg = "#b0f556", fg="#000000", width=30, height=12)
		bodylabel.config(font=(FONT, 15, STYLE))
		bodylabel.place(relx=0.5, rely=0.45, anchor="center")

		titlelabel = tk.Label(win, text="Please Confirm Details to be Correct", bg = "#b0f556", fg="black", width=30, height=2)
		titlelabel.config(font=(FONT, 20, STYLE))
		titlelabel.place(relx=0.5, rely=0.2, anchor="center")

		confirm_delete_btn = tk.Button(win, text='Confirm Deletion', padx=10, pady=10, command=lambda:delete(memId), bg='#27c0ab', borderwidth=5, relief='raised')
		confirm_delete_btn.config(font=(FONT,15,STYLE))
		confirm_delete_btn.place(relx=0.30, rely=0.8, anchor='center')

		back_to_delete_btn = tk.Button(win, text='Back to Delete Function', padx=10, pady=10, command=win.destroy, bg='#27c0ab', borderwidth=5, relief='raised')
		back_to_delete_btn.config(font=(FONT,15,STYLE), wraplength=300)
		back_to_delete_btn.place(relx=0.70, rely=0.8, anchor='center')


	win.mainloop()



## slide 8
def deleteMembersMenu():
	
	global deleteMembMenu
	global ent_memId
	deleteMembMenu = tk.Tk()
	deleteMembMenu.title("Delete Membership")
	deleteMembMenu.geometry("1920x1080")

	instructions = tk.Label(deleteMembMenu, text='To Delete Member, Please Enter Membership ID:', fg='black', bg='#c5e3e5', relief='raised', width=60, height=3)
	instructions.config(font=(FONT, FONT_SIZE, STYLE))
	instructions.place(relx=0.5, rely=0.09, anchor="center")

	lbl_memId = tk.Label(deleteMembMenu, text = "Membership ID")
	lbl_memId.config(font=(FONT, FONT_SIZE, STYLE))
	lbl_memId.place(relx=0.35, rely=0.5, anchor="center")
	ent_memId = tk.Entry(deleteMembMenu, width = 60)
	ent_memId.place(relx=0.65, rely=0.5, width = 660, height = 40, anchor="center")

	btn_deleteMember = tk.Button(deleteMembMenu, text = "Delete Member", command = deleteMember)
	btn_deleteMember.config(font=(FONT, FONT_SIZE, STYLE))
	btn_deleteMember.place(relx=0.3, rely=0.8, anchor="center")

	btn_backMembMenu = tk.Button(deleteMembMenu, text = "Back to Membership Menu", command = deleteMembMenu.destroy)
	btn_backMembMenu.config(font=(FONT, FONT_SIZE, STYLE))
	btn_backMembMenu.place(relx=0.7, rely=0.8, anchor="center")

	deleteMembMenu.mainloop()
