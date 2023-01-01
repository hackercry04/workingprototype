from flask import Flask 
from ast import literal_eval
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send,emit
import sqlite3
import colorama
from colorama import Fore
app = Flask(__name__)
# adding configuration for using a sqlite database
db = sqlite3.connect('arrays.db')
cursor = db.cursor()

x='fsdfsdfsdf'
y=2
sql_update_query = """Update numers set valuate = %s where id = 1"""
cursor.execute("Update numers set valuate = ? where id = ?",[x,y])
db.commit()
cursor.close()