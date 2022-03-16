import tkinter as tk
from PIL import ImageTk, Image
from membership_creation import createMembersMenu
from membership_deletion import deleteMembersMenu
from membership_update import updateMembersMenu
from PIL import ImageTk, Image

FONT = 'Arial'
FONT_SIZE = 25
SMALL_FONT_SIZE = 10
STYLE = 'bold'


### slide 4
def membersMenu():

	membMenu = tk.Toplevel()

	image = Image.open("bg1.jpg")
	image = image.resize((1300, 650))

	bg = ImageTk.PhotoImage(image)
	canvas1 = tk.Canvas(membMenu, width = 1920, height = 1080)
	canvas1.pack(fill = "both", expand =  True)
	canvas1.create_image(0, 0, image = bg, anchor = "nw")

	#membMenu = tk.Toplevel()
	membMenu.title("Membership")
	membMenu.geometry("1920x1080")

	instructions = tk.Label(membMenu, text='Select one of the Options below:', fg='black', bg='#c5e3e5', relief='raised', width=60, height=3)
	instructions.config(font=(FONT, FONT_SIZE, STYLE))
	instructions.place(relx=0.5, rely=0.09, anchor="center")

	btn_create = tk.Button(membMenu, text = "1. Creation", command = createMembersMenu)
	btn_create.config(font=(FONT, FONT_SIZE, STYLE))
	btn_create.place(relx=0.4, rely=0.3, anchor="center")

	desc1 = tk.Label(membMenu, text='Membership creation', fg='black')
	desc1.config(font=(FONT, FONT_SIZE, STYLE))
	desc1.place(relx=0.6, rely=0.3, anchor="center")

	btn_delete = tk.Button(membMenu, text = "2. Deletion", command = deleteMembersMenu)
	btn_delete.config(font=(FONT, FONT_SIZE, STYLE))
	btn_delete.place(relx=0.4, rely=0.45, anchor="center")

	desc2 = tk.Label(membMenu, text='Membership deletion', fg='black')
	desc2.config(font=(FONT, FONT_SIZE, STYLE))
	desc2.place(relx=0.6, rely=0.45, anchor="center")

	btn_update = tk.Button(membMenu, text = "3. Update", command = updateMembersMenu)
	btn_update.config(font=(FONT, FONT_SIZE, STYLE))
	btn_update.place(relx=0.4, rely=0.60, anchor="center")

	desc3 = tk.Label(membMenu, text='Membership update', fg='black')
	desc3.config(font=(FONT, FONT_SIZE, STYLE))
	desc3.place(relx=0.6, rely=0.60, anchor="center")

	btn_home = tk.Button(membMenu, text='Back to Main Menu', bg='#c5e3e5', relief='raised', width=60, height=1, command = membMenu.destroy)
	btn_home.config(font=(FONT, FONT_SIZE, STYLE))
	btn_home.place(relx=0.5, rely=0.80, anchor="center")

	membMenu.mainloop()

