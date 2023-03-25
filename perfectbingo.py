from flask import Flask, flash ,session,render_template,request
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
import logging
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)
# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arrays.db'

db = SQLAlchemy(app)

app.config["SESSION_TYPE"] = "filesystem"
Session(app)

logger = logging.getLogger('werkzeug')
logger.setLevel(logging.ERROR)
handler = logging.StreamHandler()
logger.addHandler(handler)
















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
    ruser = request.form['username']
    rpass = request.form['password']
    
    if len(rpass)<=4:
        flash('Password should be greater than four characters')
        return render_template("signup.html")
    
    
    elif user.query.filter_by(username=ruser).first():
        flash('Username already exists. Please choose a different username.')
        return render_template("signup.html")
    elif ruser=='' or rpass=='':  
         flash('Enter username and password')
         return render_template("signup.html")


        
    else:
        uu = user(username=ruser, password=rpass)
        db.session.add(uu)
        db.session.commit()
        return '<h1>your sign-up is succesfull </h1><a href=/login>click here</a> to login'
@app.route("/logout")
@login_required
def logout():
    

    db = sqlite3.connect('arrays.db')
    cursor = db.cursor()
        
    delete="delete from live_users where s=?"
    print(session)
    cursor.execute(delete,[session['_user_id']])
    db.commit()
    cursor.close()
    logout_user()
    return render_template('login.html')
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

        db = sqlite3.connect('arrays.db')
        cursor = db.cursor()
        #user = "select u1,u2 from roomgroup where roomname=?"
        add_live_user="insert into live_users(users,s) values(?,?)"
        check="select count(*) from live_users where users=?"
        print('hereis t',cursor.execute(check,[username]).fetchall()[0][0])
        if cursor.execute(check,[username]).fetchall()[0][0]==0:
           cursor.execute(add_live_user,[username,session['_user_id']])
           db.commit()
        cursor.close()

        
        
        return home()
    elif password=='':
        flash("enter the password.")
        return render_template("login.html")   
        
    else:
        flash("incorrect username or password.")
        return render_template("login.html")   
@app.route("/profile")
@login_required
def current():
    
    return 'currentuser is '+u.username

@app.route("/online")
@login_required
def online():
    return render_template('online.html')



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

@app.route("/home")
@login_required
def home():
    return render_template("/home.html")



@app.route("/invites")
@login_required
def invitepage():
    return render_template("/invites.html")    

@login_required
@app.route("/delete")
def delete():
   room = request.args.get('room')
   id=session['_user_id']

   db = sqlite3.connect('arrays.db')
   cursor = db.cursor()
   #user = "select u1,u2 from roomgroup where roomname=?"
   delete_room="delete from rooms where roomn=?"
   #delete_room_group="delete from roomgroup where roomname=?"
   delete_room_group_user="delete  from roomgroup where roomname=? and u1=? or u2=?"
   delete_u='delete from numers where usession=?'
   print("room is",room)
   #u=cursor.execute(user,[room]).fetchall()
   cursor.execute(delete_room,[room])
   cursor.execute(delete_room_group_user,[room,id,id])

   cursor.execute(delete_u,[id])
   

  
   db.commit()
   cursor.close()
   #print('deleted users are',u1,u2)
   return 0


       
##















##socket start

turn=1

f1=f2=f3=f4=f5=f6=f7=f8=f9=f10=f11=f12=0







state="not bingo"
socketio = SocketIO(app, cors_allowed_origins='*')
state="not_bingo"


user1=[]
user2=[]

def insertuserstogroup(room,uid,session):
    #check='select count(*) from roomgroup where roomname=?'
    print("uid iside function is",uid)
    check='select count(*) from roomgroup where roomname=?'
    db = sqlite3.connect('arrays.db')
    cursor = db.cursor()
    if(cursor.execute(check,[room]).fetchall()[0][0]==0):

       if uid=='1':
          print("this worked in user1 in db")

          sql_command="INSERT INTO roomgroup(roomname,u1) VALUES(?,?)"
          cursor.execute(sql_command,[room,session])
          db.commit()
          cursor.close()
          return 0
       elif uid=='2':
          print("uid 2 worked in db") 
          sql_command="INSERT INTO roomgroup(roomname,u2) VALUES(?,?)"
          cursor.execute(sql_command,[room,session])
          db.commit()
          cursor.close()
          return 0

    elif uid=='1':
        sql_command='update roomgroup set u1=? where roomname=?'   
    elif uid=='2':
        sql_command='update roomgroup set u2=? where roomname=?' 


    cursor.execute(sql_command,[session,room])
          
    db.commit()
    cursor.close()

        
    return 0




def get_users_from_group(room):
    qu1='select u1 from roomgroup where roomname=?'
    qu2='select u2 from roomgroup where roomname=?'
    db = sqlite3.connect('arrays.db')
    cursor = db.cursor()
    u1=cursor.execute(qu1,[room]).fetchall()[0][0]
    u2=cursor.execute(qu2,[room]).fetchall()[0][0]
    u1=int(u1)
    u2=int(u2)
    db.commit()
    cursor.close()
    return u1,u2











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

def storingarraytodb(array):
   s=session['_user_id']

   db = sqlite3.connect('arrays.db')
   cursor = db.cursor()
   sql_update_query = "INSERT INTO numbers(usession,numberarray)  VALUES(?,?)"
   check='select count(*) from numbers where usession=?'
   
   if(cursor.execute(check,[s]).fetchall()[0][0]==0):
   
     
     cursor.execute(sql_update_query,[s,str(array)])
     db.commit()
     cursor.close()
    
   
   return 0

def removearrays():
   s=session['_user_id']

   db = sqlite3.connect('arrays.db')
   cursor = db.cursor()
   sql_update_query = "delete from numbers where id=?"
   
   
  
   
     
   cursor.execute(sql_update_query,[s])
   db.commit() 
   cursor.close()
    
   
   return 'success'



def updating(i,arr):
    db = sqlite3.connect('arrays.db')
    cursor = db.cursor()
    i=str(i)
    arr=str(arr)
    sql_update_query = "Update numers set valuate = ? where usession= ?"
    cursor.execute(sql_update_query,[arr,i])
    db.commit()
    cursor.close()
    
    
def getarray_with_id(id):
    
    db = sqlite3.connect('arrays.db')
    cursor = db.cursor()
    getquery="SELECT valuate FROM numers where usession=?"
    f=cursor.execute(getquery,[id]).fetchall()

    if (f!=[]):
       f=literal_eval(f[0][0])
    print(f)
    db.commit()
    cursor.close()
    return f

def getnumberarray_with_id(id):
    
    db = sqlite3.connect('arrays.db')
    cursor = db.cursor()
    getquery="SELECT numberarray FROM numbers where usession=?"
    f=cursor.execute(getquery,[id]).fetchall()

    if (f!=[]):
       f=literal_eval(f[0][0])
    print(f)
    db.commit()
    cursor.close()
    return f



def valuating(v,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12):
            u="null"
            global state
           
            
            
            
            
            
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

            print("the function values for ")
            print(v)
            print(f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,state,u)
            return(f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,state,u)


@login_required
@socketio.on('message')
def handleMessage(m,roomname,userid): 
    join_room(roomname)
    print(m)
    print('user entered the room====',   roomname)
    print("user id is ",userid)
    adding0array(session['_user_id'])
    print("added arry of 0 s to database ")
    insertuserstogroup(roomname,userid,session['_user_id'])
    ##sending turn 
    updateturn(roomname,1)
    turn=getturn(roomname)
    print("sdkfsodjfisdhjfhsdakjhfkjsdhjksgdhgsdhj",turn)
    
    socketio.emit('turn',turn,to=roomname)


@socketio.on('storearrays')

def storearrayes(exnum):
    storingarraytodb(exnum)




    
    
    
    
    


















#user one
@socketio.on('values')
def num(x):
    global user1
    user1=x
    
    print("exnum array: ",x)
@socketio.on('clicked') # when user1 clicks a button
def click(index,n,id,roomname):
    f1=f2=f3=f4=f5=f6=f7=f8=f9=f10=f11=f12=0
    global clicked ,user1
    clicked=n
    print("user1 clciked number is: ",n,"and id is:  ",id," with index", index)
    print("user2 is=",user2)
    #retrieving values from db
    print("get_users_from_roomname",get_users_from_group(roomname)) #get user ids with room name(the is is stored in pairs with room name as its heading)
    #geting user with room name
    u1,u2=get_users_from_group(roomname)
    #----------------------------
    valuate=getarray_with_id(u1)
    valuate1=getarray_with_id(u2)
    valuate[index]=1
    print("valuate,valuate 1 is",valuate,valuate1)
    valuate1[user2.index(n)]=1 #to find the position of 0 in [00000 ] array and make it 1

    #inserting the updated array to db with ids
    updating(u1,valuate)
    updating(u2,valuate1)

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
   
    join_room(str(u1)+'r')
    print(str(u1)+" joined the room "+str(u1)+'r')
   
    socketio.emit('statics',[valuating(valuate,0,0,0,0,0,0,0,0,0,0,0,0)],to=str(u1)+'r')
    print(' u1 ',[valuating(valuate,0,0,0,0,0,0,0,0,0,0,0,0)])
    socketio.emit('statics',[valuating(valuate1,0,0,0,0,0,0,0,0,0,0,0,0)],to=str(u2)+'r')
    print(' u2 ',[valuating(valuate,0,0,0,0,0,0,0,0,0,0,0,0)])
   
#----chat in game
@socketio.on('chat-in-game')
def chat_in(roomname,chit,iid):
    print(chit)
    socketio.emit('chat-response',[chit,iid],to=roomname)

#-----chat in game 


    

#----------------------------------

#user two 
@socketio.on('values2')
def num2(x):
    global user2
    user2=x
    
    print("user2 exnum array: ",x,flush=True)
@socketio.on('clicked2') #when user 2 clicked a button
def click2(index,n1,id,roomname):
    global clicked2
    clicked2=n1
    print("user2 clciked number is: ",n1,"and id is:  ",id," with index: ",index,flush=True)
    #retrieving values from db
    #getting users with roomname
    u1,u2=get_users_from_group(roomname)
    #----------------------------------
    valuate=getarray_with_id(u1)
    valuate1=getarray_with_id(u2)
    valuate1[index]=1
    valuate[user1.index(n1)]=1
    #inserting the updated array to db with ids
    updating(u1,valuate)
    updating(u2,valuate1)

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
    

   
    print("valuatin",valuating(valuate1,0,0,0,0,0,0,0,0,0,0,0,0))
    print("valuatin2",valuating(valuate,0,0,0,0,0,0,0,0,0,0,0,0))
    
   
    #valuating values-----------------
  #sending back possible matched bingo lines ,with state and user id

    join_room(str(u2)+'r')
    print(str(u2)+"joined the room "+str(u2)+'r')
   
    socketio.emit('statics',[valuating(valuate1,0,0,0,0,0,0,0,0,0,0,0,0)],to=str(u2)+'r')
    socketio.emit('statics',[valuating(valuate,0,0,0,0,0,0,0,0,0,0,0,0)],to=str(u1)+'r')
    
#------------------------------------


def add_online_users():
    db = sqlite3.connect('arrays.db')
    cursor = db.cursor()
    t="nothing"
    check='select count(*) from online where u=?'
    insert="insert into online(u) values(?)"
    get_query="select users from live_users where s=? "
    user=cursor.execute(get_query,[session['_user_id']]).fetchall()[0][0]
    select_all="select u from online"


    print(user)
    
    
    if(cursor.execute(check,[user]).fetchall()[0][0]==0):
            
            cursor.execute(insert,[user])
            
            db.commit()
            


    all_users=cursor.execute(select_all).fetchall()
    cursor.close()       
    return all_users


def delete_online_user():
    db = sqlite3.connect('arrays.db')
    cursor = db.cursor()
    get_query="select users from live_users where s=? "
    user=cursor.execute(get_query,[session['_user_id']]).fetchall()[0][0]
    f="delete from online where u=?"
    cursor.execute(f,[user])
    db.commit()
    cursor.close()




def store_invite(room,uname):
    db=sqlite3.connect('arrays.db')
    cursor=db.cursor()
    insert="insert into invites(roomname,uname,hostname) values(?,?,?)"
    get_host="select username from user where id=?"
    host=cursor.execute(get_host,[session['_user_id']]).fetchall()[0][0]
    check="select count(*) from invites where uname=? and hostname=?";

    if uname!=host: #and (cursor.execute(check,[uname,host]).fetchall()[0][0]==0)

       cursor.execute(insert,[room,uname,host])
    db.commit()
    cursor.close()



def send_back_invites():
    id=session['_user_id']
    db=sqlite3.connect('arrays.db')
    cursor=db.cursor()
    get_user_name="select username from user where id=?"
    get_room="select * from invites where uname=? "
    user_id=cursor.execute(get_user_name,[id]).fetchall()[0][0]
    print("fjksdhjfhjskd",user_id)
    roomname=cursor.execute(get_room,[user_id]).fetchall()
    
    print("dfsfdsf",roomname)

    db.commit()
    cursor.close()
    return roomname
def get_name():
    id=session['_user_id']
    db=sqlite3.connect('arrays.db')
    cursor=db.cursor()
    get_user_name="select username from user where id=?"

    user_id=cursor.execute(get_user_name,[id]).fetchall()[0][0]
    db.commit()
    cursor.close()
    
    return user_id

def remove_invites(r):
    db=sqlite3.connect('arrays.db')
    cursor=db.cursor()
    delete_link="delete from invites where roomname=?"
    cursor.execute(delete_link,[r])
    db.commit()
    cursor.close()


def invite_count():
    db=sqlite3.connect('arrays.db')
    cursor=db.cursor()
    name=get_name()
    join_room(name)
    get_count="select count(*) from invites where uname=?"
    c=cursor.execute(get_count,[name]).fetchall()[0][0]
    db.commit()
    cursor.close()
    return c,name



#online users------------------------------------------------
@login_required
@socketio.on('message',namespace='/onlineusers')
def onlidf(msg):
    print('chat online connected',msg)
    u=add_online_users()
    socketio.emit("users",u,namespace='/onlineusers')
    print('emitted users')


@socketio.on('disconnect',namespace='/onlineusers')
def disconnect():
    print("client disconnecte d")
    delete_online_user()



@socketio.on('disconnect')
def disconnectdb():
    print("client disconnecte d")
    removearrays()    

@socketio.on('invite',namespace='/onlineusers')
def storeinvite(room,uname):
    store_invite(room,uname)


@socketio.on('sendingmsg',namespace='/onlineusers')
def sendmessage(msg):
    print(msg)
    n=get_name()
    print("here is the user name",n)
    socketio.emit('fast',[n,msg],namespace='/onlineusers')


@login_required
@socketio.on('message',namespace='/sendinvite')
def sendinvite(msg):
    print('chat online connected',msg)
    r=send_back_invites()
    join_room(r[0][2])
    socketio.emit("users",send_back_invites(),namespace='/sendinvite',to=r[0][2])
    print(r[0][2],"socketrito")
    leave_room(r[0][2])
    

@socketio.on('removelink',namespace='/sendinvite')
def removelink(r):
    remove_invites(r)
    




    

#online users-------------------------------------------------










##befor starting the game ,controls the online offline activity of users 

    
@login_required
@socketio.on('message',namespace='/onlinestatus')
def onstatus(msg):
    print('chat online connected------------------------------------------------',msg)




@socketio.on('status',namespace='/onlinestatus')

def ss(r,u):
        
    join_room(r)
    socketio.emit('st',u,to=r,namespace='/onlinestatus')
    
  #get request to identify disconnect and start  
@login_required
@app.route("/dis")
def dicon():
    room=request.args.get('room')
    print('room is going to disconnect ',room)
    socketio.emit('st','disconnected',to=room,namespace='/onlinestatus')
    leave_room(room)

    return 'success'

@login_required
@app.route("/startss")
def msg_start():
    room=request.args.get('room')
    print('user started the gam ein the room ',room)
    socketio.emit('st','started',to=room,namespace='/onlinestatus')
    leave_room(room)

    return 'success'
#----------------------------------------------------------
    

@socketio.on('bingo-w')
def won(u,r):

    print('we won fhsjdkhfsdjhfjaksdhjfgsdhjfgsjdhfsjdhfiusdghiufsdiufysdi')
    socketio.emit('bingo-win',u,to=r)


#invite count

@socketio.on('count',namespace='/onlineusers')
def fc():
 
    c,n=invite_count()
   
    socketio.emit('cou',c,namespace='/onlineusers',to=n)
    leave_room(n)























  
if __name__ == '__main__':
	socketio.run(app)
