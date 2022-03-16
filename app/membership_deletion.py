import sqlalchemy as db
import tkinter as tk
from datetime import *

FONT = 'Arial'
FONT_SIZE = 25
SMALL_FONT_SIZE = 10
STYLE = 'bold'

USERNAME = "root"
PASSWORD = "Crunchyapples99"
HOST = "localhost"
PORT = 3306
DB = "Library"

engine = db.create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(USERNAME, PASSWORD, HOST, PORT, DB), echo = False)
cursor = engine.connect()


def delete(idinput):
	delete_member = "DELETE FROM Members WHERE memberId = '{}'".format(idinput)
	cursor.execute(delete_member)

	deletepopup = tk.Tk()
	label1 = tk.Label(deletepopup, text='Membership deleted', fg='black', bg='#c5e3e5', relief='raised', width=60, height=3)
	label1.pack()

	btn_back = tk.Button(deletepopup, text = "Back", command = lambda: [deletepopup.destroy(), win.destroy()])
	btn_back.pack()
	
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

	if len(memberInfo) == 0:
		label1 = tk.Label(win, text='Error: No such member found', fg='black', bg='#c5e3e5', relief='raised', width=60, height=3)
		label1.pack()

		btn_back = tk.Button(win, text = "Back", command = win.destroy)
		btn_back.pack()
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
		label1 = tk.Label(win, text="Error!", bg="#cc0505", fg= "#ffff00")
		label1.pack()
		label2 = tk.Label(win, text="Member has loans, reservations or outstanding fines.")
		label2.pack()
		btn = tk.Button(win, text="Back to Delete Function", command=win.destroy)
		btn.pack()

	# success, deletion SQL, reservations cascade in SQL
	else:

		memberInfo = "Member ID: {}\nName: {}\nFaculty: {}\nPhone Number: {}\nEmail Address: {}".format(memId, name, faculty, phoneNo, email)

		titlelabel = tk.Label(win, text="Please Confirm Details to be Correct", bg ="#9ddd58", fg="black", width=30, height=2)
		titlelabel.config(font=(FONT, FONT_SIZE, STYLE))
		titlelabel.place(relx=0.5, rely=0.3, anchor="center")
		#titlelabel.pack()

		bodylabel = tk.Label(win, text=memberInfo, fg="#000000", width=30, height=12)
		bodylabel.config(font=(FONT, FONT_SIZE, STYLE))
		bodylabel.place(relx=0.5, rely=0.55, anchor="center")

		confirm_delete_btn = tk.Button(win, text='Confirm Delete', padx=10, pady=10, command=lambda:delete(memId), bg='#27c0ab', borderwidth=5, relief='raised')
		confirm_delete_btn.config(font=(FONT,20,STYLE))
		confirm_delete_btn.place(relx=0.35, rely=0.8, anchor='center')

		back_to_delete_btn = tk.Button(win, text='Back to Delete Function', padx=10, pady=10, command=win.destroy, bg='#27c0ab', borderwidth=5, relief='raised')
		back_to_delete_btn.config(font=(FONT,20,STYLE), wraplength=300)
		back_to_delete_btn.place(relx=0.65, rely=0.8, anchor='center')


	win.mainloop()



## slide 8
def deleteMembersMenu():
	
	global deleteMembMenu
	global ent_memId
	deleteMembMenu = tk.Tk()
	deleteMembMenu.title("Delete Membership")

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
