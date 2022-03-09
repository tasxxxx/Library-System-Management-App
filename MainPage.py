# from sqlalchemy import create_engine
import tkinter as tk
import sqlalchemy as db
import pandas as pd
from PIL import ImageTk, Image 
from datetime import datetime, date
from turtle import width
from dateutil.relativedelta import relativedelta

root = tk.Tk()
root.title("A Library System (ALS)")

## 1 MAIN MENU ##
def destroyMainMenu():
	mainMenu.destroy()

def mainMenuF():
	global mainMenu
	mainMenu = tk.Toplevel()
	mainMenu.title("Main Menu")
	mainMenu.geometry("1280x720")

	memButton = tk.Button(mainMenu, text = "Membership")
	booksButton = tk.Button(mainMenu, text = "Books")
	loansButton = tk.Button(mainMenu, text = "Loans")
	resButton = tk.Button(mainMenu, text = "Reservations")
	finesButton = tk.Button(mainMenu, text = "Fines")
	repsButton = tk.Button(mainMenu, text = "Reports")

	memButton.place(x = 280, y = 100, width = 300, height = 170)
	booksButton.place(x = 630, y = 100, width = 300, height = 170)
	loansButton.place(x = 980, y = 100, width = 300, height = 170)
	resButton.place(x = 280, y = 550, width = 300, height = 170)
	finesButton.place(x = 630, y = 550, width = 300, height = 170)
	repsButton.place(x = 980, y = 550, width = 300, height = 170)


mainMenuF()
root.mainloop()