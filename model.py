from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
app = Flask(__name__)
app.debug = True
# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arrays.db'
db = SQLAlchemy(app)

class numers(db.Model):
    id=db.Column(db.Integer,primary_key=True)


    usession=db.Column(db.String(50),unique=True) 
    valuate=db.Column(db.String(50)) 
class rooms(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    roomn=db.Column(db.String(50),unique=True)
    uturn=db.Column(db.Integer)

class roomgroup(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    roomname=db.Column(db.String(50),unique=True)
    u1=db.Column(db.Integer) 
    u2=db.Column(db.Integer)     
    

class user(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True)
    password=db.Column(db.String(20))    

class live_users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    users=db.Column(db.String(50),unique=True)
    s=db.Column(db.String(10),unique=True)


class online(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    u=db.Column(db.String(50),unique=True)


class invites(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    roomname=db.Column(db.String(10))  
    uname=db.Column(db.String(10))
    hostname=db.Column(db.String(10))



class numbers(db.Model):
    id=db.Column(db.Integer,primary_key=True)


    usession=db.Column(db.String(50),unique=True) 
    numberarray=db.Column(db.String(50))   


# Creating an SQLAlchemy instance
db.create_all()


if __name__ == '__main__':
   app.run()