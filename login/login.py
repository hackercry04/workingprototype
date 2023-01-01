from flask import Flask,render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required,current_user
 
app = Flask(__name__)
app.debug = True
 
# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SECRET_KEY']="secret"
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

app.config["SESSION_TYPE"] = "filesystem"
Session(app)
 
login_manager=LoginManager()
login_manager.init_app(app)

class user(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True)
    password=db.Column(db.String(20))

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
        print("session is",session['_user_id'])
        return 'user logged in '
    elif password=='':
        return 'enter the password'
    else:
        return 'no user found'    
@app.route("/profile")
@login_required
def current():
    
    return 'currentuser is '+u.username


if __name__ == '__main__':
    app.run()