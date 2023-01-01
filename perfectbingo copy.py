from flask import Flask ,session,render_template,request
from ast import literal_eval
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send,emit,join_room, leave_room
from model import db,numers,rooms,user
from flask_session import Session
import colorama
import sqlite3
from termcolor import colored
from colorama import Fore
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required,current_user
app = Flask(__name__)
# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arrays.db'

db = SQLAlchemy(app)

app.config["SESSION_TYPE"] = "filesystem"
Session(app)


##login functionality

# adding configuration for using a sqlite database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
#app.config['SECRET_KEY']="secret"
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

app.config["SESSION_TYPE"] = "filesystem"
Session(app)
 
login_manager=LoginManager()
login_manager.init_app(app)

#class user(UserMixin,db.Model):
    #id=db.Column(db.Integer,primary_key=True)
    #username=db.Column(db.String(20),unique=True)
    #password=db.Column(db.String(20))

@login_manager .user_loader
def load_user(user_id):
    return user.query.get(int(user_id)) 


@app.route("/signup")
def sign():
    return render_template("signup.html")

@app.route("/reg",methods=['POST'])
def register():
    ruser=request.form['username']
    rpass=request.form['password']
    uu=user(username=ruser,password=rpass)
    db.session.add(uu)
    db.session.commit()
    return '<h1>your sign-up is succesfull </h1><a href=/login>click here</a> to login'
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return 'you are logged out'
@app.route("/login")
def login():
    return render_template('login.html')
@app.route("/logmein",methods=["POST"])
def logme():
    global u
    username=request.form['username']
    password=request.form['password']
    print(password)
    u=user.query.filter_by(username=username,password=password).first()  
    if u:
        login_user(u)
        ##holy fuck here is the session
        
        return link()
    elif password=='':
        return 'enter the password'
    else:
        return 'no user found'    
@app.route("/profile")
@login_required
def current():
    
    return 'currentuser is '+u.username

@app.route("/linkgen")
@login_required
def link():
    return render_template('linkgen.html')

@app.route("/game")
@login_required
def game():
    return render_template('game.html')
@app.route("/bingo")
@login_required
def bingo():
    return render_template('bingo1.html')
##














##socket start

turn=1






f1=f2=f3=f4=f5=f6=f7=f8=f9=f10=f11=f12=0
state="not bingo"
socketio = SocketIO(app, cors_allowed_origins='*')


user1=[]
user2=[]


def updateturn(roomname,turns):
    t="nothing"
    check='select count(*) from rooms where roomn=?'
    db = sqlite3.connect('arrays.db')
    cursor = db.cursor()
   
    sql_update_query = "INSERT INTO rooms(roomn,uturn) VALUES(?,?)"
    print("rahsi",cursor.execute(check,[roomname]).fetchall()[0][0])
    if(cursor.execute(check,[roomname]).fetchall()[0][0]==0):
            print("this part is working")
            cursor.execute(sql_update_query,[roomname,turns])
            
            db.commit()

    else:
        turnupdate="Update rooms set uturn = ? where roomn = ?"       
        cursor.execute(turnupdate,[turns,roomname])
        db.commit()
    cursor.close()
    
    return t

def getturn(roomname):
    db = sqlite3.connect('arrays.db')
    cursor = db.cursor()
    
    sql_update_query = "SELECT uturn FROM rooms where roomn=?"
    t=cursor.execute(sql_update_query,[roomname]).fetchall()
    
    t=t[0][0]
    print("fsdf",t)
    db.commit()
    cursor.close()

    return int(t)




def adding0array(s):

   db = sqlite3.connect('arrays.db')
   cursor = db.cursor()
   sql_update_query = "INSERT INTO numers(usession,valuate)  VALUES(?,?)"
   check='select count(*) from numers where usession=?'
   print("jsdfsdhfjkhsdjk",cursor.execute(check,[s]).fetchall()[0][0])
   if(cursor.execute(check,[s]).fetchall()[0][0]==0):
   
     v= "[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]"
     cursor.execute(sql_update_query,[s,v])
     db.commit()
     cursor.close()
    
   
   return 0


def updateturns(roomname,turn):
    

    return 0   

def updating(i,arr):
    db = sqlite3.connect('arrays.db')
    cursor = db.cursor()
    i=str(i)
    arr=str(arr)
    sql_update_query = "Update numers set valuate = ? where id = ?"
    cursor.execute(sql_update_query,[arr,i])
    db.commit()
    cursor.close()
    
    
def getarray_with_id(id):
    
    db = sqlite3.connect('arrays.db')
    cursor = db.cursor()
    getquery="SELECT valuate FROM numers where id=?"
    f=cursor.execute(getquery,[id]).fetchall()
    f=literal_eval(f[0][0])
    db.commit()
    cursor.close()
    return f

    
def valuating(v,u):
            global f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,state
            
            print(v[1]+v[2]+v[3]+v[4]+v[5])
            if (v[1]+v[2]+v[3]+v[4]+v[5]==5):
                f1=1
            if (v[6]+v[7]+v[8]+v[9]+v[10]==5):
                f2=1
            if (v[11]+v[12]+v[13]+v[14]+v[15]==5):
                f3=1  
            if (v[16]+v[17]+v[18]+v[19]+v[20]==5):
                f4=1 
            if (v[21]+v[22]+v[23]+v[24]+v[25]==5):
                f5=1
            if (v[1]+v[7]+v[13]+v[19]+v[25]==5):
                f6=1 
            if (v[5]+v[9]+v[13]+v[17]+v[21]==5):
                f7=1
            if (v[1]+v[6]+v[11]+v[16]+v[21]==5):
                f8=1
            if (v[2]+v[7]+v[12]+v[17]+v[22]==5):
                f9=1
            if (v[3]+v[8]+v[13]+v[18]+v[23]==5):
                f10=1
            if (v[4]+v[9]+v[14]+v[19]+v[24]==5):
                f11=1
            if (v[5]+v[10]+v[15]+v[20]+v[25]==5):
                f12=1
            if (f1+f2+f3+f4+f5+f6+f7+f8+f9+f10+f11+f12>=5):
                print("BINGO",flush=True)
                state="bingo"
            print(v,flush=True)
            return(f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,state,u)


@login_required
@socketio.on('message')
def handleMessage(m,roomname): 
    join_room(roomname)
    print('user entered the room====',   roomname)
    print(m)
    adding0array(session['_user_id'])
    print("added arry of 0 s to database ")
    ##sending turn 
    updateturn(roomname,1)
    turn=getturn(roomname)
    print("sdkfsodjfisdhjfhsdakjhfkjsdhjksgdhgsdhj",turn)
    
    socketio.emit('turn',turn,to=roomname)
    
    
    
    
    

















#user one
@socketio.on('values')
def num(x):
    global user1
    user1=x
    
    print("exnum array: ",x)
@socketio.on('clicked')
def click(index,n,id,roomname):
    global clicked ,user1
    clicked=n
    print("user1 clciked number is: ",n,"and id is:  ",id," with index", index)
    print("user2 is=",user2)
    #retrieving values from db

    valuate=getarray_with_id(1)
    valuate1=getarray_with_id(2)
    valuate[index]=1
    print("valuate,valuate 1 is",valuate,valuate1)
    valuate1[user2.index(n)]=1

    #inserting the updated array to db with ids
    updating(1,valuate)
    updating(2,valuate1)

    print(colored("(user1)valuate","green"),valuate)
    
    print(colored("(user1)valuate1","green"),valuate1)
    print(session)
    print(getarray_with_id(1))
    #print(valuating(valuate,0))
    #print(valuating(valuate1,1))
    socketio.emit('light',n,to=roomname)
    #print("light sended")
     #print("light sended")
    #global turn 
    #update turn and storing
    turn=getturn(roomname)
    turn=turn+1
    updateturn(roomname,turn)
    #----------------
    socketio.emit('turn',turn,to=roomname)
    print("turn is ",turn)
    
    

#----------------------------------

#user two 
@socketio.on('values2')
def num2(x):
    global user2
    user2=x
    
    print("user2 exnum array: ",x,flush=True)
@socketio.on('clicked2')
def click2(index,n1,id,roomname):
    global clicked2
    clicked2=n1
    print("user2 clciked number is: ",n1,"and id is:  ",id," with index: ",index,flush=True)
    #retrieving values from db
    valuate=getarray_with_id(1)
    valuate1=getarray_with_id(2)
    valuate1[index]=1
    valuate[user1.index(n1)]=1
    #inserting the updated array to db with ids
    updating(1,valuate)
    updating(2,valuate1)

    print(colored("(user2)valuate","green"),valuate)
    print(session)
    print(colored("(user2)valuate1","green"),valuate1)
    #print(valuating(valuate,0))
    #print(valuating(valuate1,1))
    socketio.emit('light',n1,to=roomname)
    #print("light2 sended",flush=True)
   
    #updaing and storing turn
    turn=getturn(roomname)
    turn=turn+1
    updateturn(roomname,turn)
    #--------------------------
    print("turn is ",turn,flush=True)
    socketio.emit('turn',turn,to=roomname)
    



    #valuating values-----------------
  #sending back possible matched bingo lines ,with state and user id
    socketio.emit('states',valuating(valuate,0),to=roomname)
#------------------------------------

































  
if __name__ == '__main__':
	socketio.run(app)
