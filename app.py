# Virtual ENV source ~/Projects/NLP/bin/activate

from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,UserMixin,logout_user
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medbooking.db'
app.config['SECRET_KEY'] = 'thisissecret'
db = SQLAlchemy(app)

# Create login manger object and initialise it with app
login_manager = LoginManager()
login_manager.init_app(app)

## Create Model User
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fname = db.Column(db.String(120), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    passwd = db.Column(db.String(120), nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username

### Create model to save the eqnquiries

class Reservation(db.Model):
    res_id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80), unique=True, nullable=False)
    location = db.Column(db.String(80), nullable=False)
    details = db.Column(db.Text(), nullable=False)
    pub_date = db.Column(db.DateTime(), nullable=False,default=datetime.utcnow())

    def __repr__(self):
        return '<Reservation %r>' % self.fullname

# Create User loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
### Read the reservation data and render it to the homepage
    data=Reservation.query.all()
    return render_template("index.html", data=data)

@app.route("/main")
def main():
    return render_template("main.html")

## Define methods in Register
@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=='POST':
        email = request.form.get('email')
        username = request.form.get('username')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        passwd = request.form.get('passwd')
        user = User(username=username,email=email,fname=fname,lname=lname,passwd=passwd)
        db.session.add(user)
        db.session.commit()
        flash('User has registered successfully','success')
        return redirect('/login')
    
    return render_template("register.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form.get('username')
        passwd = request.form.get('passwd')
        user = User.query.filter_by(username=username).first()
        if user and passwd==user.passwd:
            login_user(user)
            return redirect('/')
        else:
            flash('Invalid credentials','danger')
            return redirect('/login')
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')

@app.route("/reservation",methods=['GET','POST'])
def reservation():
    if request.method=='POST':
        fullname = request.form.get('fullname')
        location = request.form.get('location')
        details = request.form.get('details')
        reservation = Reservation(fullname=fullname,location=location,details=details)
        db.session.add(reservation)
        db.session.commit()
        flash('Your request has been submitted','success')
        return redirect('/')
    return render_template("reservation.html")


## If flask give OSError: [Errno 48] Address already in use
### Use following command lsof -i:5000 and killed respective PID
if __name__=='__main__':
    app.run(debug=True)
