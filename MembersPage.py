#from sqlalchemy import create_engine
import tkinter as tk
import sqlalchemy as db
import pandas as pd

# from apps.resources.variables import *
# from apps.resources.container import Container

#USER = 'root'
#PASSWORD = 'Crunchyapples99'
#HOST = 'localhost'
#PORT = 3306
#DATABASE = 'Library'

# pymysql
#engine = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(
#            USER, PASSWORD, HOST, PORT, DATABASE))

# SQLAlchemy
# dialect+driver://username:password@host:port/database
# engine = db.create_engine("root://root:Crunchyapples99@localhost:3306/Library", echo = True)
engine = db.create_engine("mysql://root:Crunchyapples99@localhost:3306/Library", echo = True)

cursor = engine.connect()
metadata = db.MetaData()

members = db.Table('Members', metadata, autoload = True, autoload_with = engine)
book = db.Table('Book', metadata, autoload = True, autoload_with = engine)
fine = db.Table('Fine', metadata, autoload = True, autoload_with = engine)
author = db.Table('Author', metadata, autoload = True, autoload_with = engine)
reservation = db.Table('Reservation', metadata, autoload = True, autoload_with = engine)
borrow = db.Table('Borrow', metadata, autoload = True, autoload_with = engine)

sql_statement = """SELECT FROM Members"""