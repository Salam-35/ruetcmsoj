from datetime import datetime
# from sqlalchemy import SQLAlchemy
from flask import *
from forms import RegistrationForm, LoginForm
import pyrebase
import sys
import os
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# db = SQLAlchemy()

app.secret_key = os.urandom(24)

# class User(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     username=db.Column(db.String(20),unique=True,nullable=False)
#     email=db.Column(db.String(120),unique=True,nullable=False)
#     image_file=db.Column(db.String(20),unique=False,nullable=False,default='dp.img')
#     password=db.Column(db.String(60),unique=False,nullable=False)

#     def __repr__(self):
#         return f"User('{self.username}','{self.email}')"

# class Post(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
    
#     content=db.Column(db.Text)
#     title=db.Column(db.String(20),nullable=False)
#     date_posted=db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    
#     def __repr__(self):
#         return f"User('{self.title}','{self.date_posted}')"

# def create_app():
#     app = Flask(__name__)
#     db.init_app(app)
#     return app
# firebase = FirebaseApplication("https://ruetcms.firebaseio.com/",None)

config = {
    "apiKey": "AIzaSyC_KXG8Vx3kD5MXDXz-dKWAYcG9xlehW6Y",
    "authDomain": "ruetcms.firebaseapp.com",
    "databaseURL": "https://ruetcms.firebaseio.com",
    "projectId": "ruetcms",
    "storageBucket": "ruetcms.appspot.com",
    "messagingSenderId": "102610020548",
    "appId": "1:102610020548:web:d052428fa510f293150191",
    "measurementId": "G-XR5WZPP629"
}
firebase = pyrebase.initialize_app(config)
#auth instance
auth = firebase.auth()
#real time database instance
db = firebase.database();


RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
CLIENT_SECRET = '6eac0eba6c92665528a8c24b44781c74e3922079'

posts = [
    {
        'author': 'Salam_35',
        'title': 'Bad Story',
        'content': 'First post content',
        'id': '00001',
        'date_posted': 'July 20, 2020'
    },
    {
        'author': 'joynahiid',
        'title': 'Yet Another Travelling Problem',
        'content': 'Second post content',
        'id':'00002',
        'date_posted': 'July 20, 2020'
    }
]


@app.route("/")
@app.route("/home")
def home():
    # print("print current user "+ current_user)
    return render_template('home.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username=form.username.data
        email=form.email.data
        password=form.password.data
        print(username)
        print(email)
        print(password)

        try:
            auth.get_user_by_email(email)
            flash(f'''Already registered with this email''', 'danger')
            return render_template('register.html')
        except:
            pass

        try:
            cuser=db.child("user").child(username).get()
            flash(f'''Already registered with this User Name {username}''', 'danger')
            return render_template('register.html')
        except:
            pass

        try:
            auth.create_user_with_email_and_password(email, password);
            user = auth.sign_in_with_email_and_password(email,password) 
            # print(user['localId'])

            user['displyName']: username

            # print("user.displyName is ")
            # print(user.displyName)
            data = {
            "username": username,
            "email": email,
            "userid":user['localId']
            }
            db.child("users").child(username).set(data)
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
        except:
            flash(f'Account cant be created for {form.username.data}! ', 'danger')
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        email=form.email.data
        password=form.password.data
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            # set the session
            user_id = user['idToken']
            user_email = email
            session['usr'] = user_id
            session["email"] = user_email

            # print(user)

            flash('Welcome back!', 'success')
            return redirect(url_for('home'))
        except:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    else:
        return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():   
    print("logging out--------------------------------")
    print(session["email"])
    auth.current_user = None
    #also remove the session
    #session['usr'] = ""
    #session["email"] = ""
    em=session["email"]
    session.clear()
    flash(f'Good bye { em }!','success')
    return redirect("/");


@app.route("/comming_contest")
def comming_contest():
    return render_template('contests.html')
@app.route("/profile")
def profile():
    return render_template('profile.html')



@app.route("/showproblem/<problem_id>")
def showproblem(problem_id):
    print(problem_id)
    for x in posts:
        if x['id']==problem_id:
            return render_template('show_problem.html',post=x)

@app.route("/submit_problem/<problem_id>",methods=['GET', 'POST'])
def submit_problem(problem_id):
    print(request.method)
    if request.method=="POST":
        code=request.form['source_code']
        print(code)
        language=request.form['solveLanguage']
        print(request.form['solveLanguage'])
        

        data = {
        'client_secret': CLIENT_SECRET,
        'async': 0,
        'source': code,
        'lang': "CPP14",
        'time_limit': 5,
        'memory_limit': 262144,
        }



        # print(data)
        r = requests.post(RUN_URL, data=data)
        output=r.json()
        print(output['run_status']['output'])
        print(r.json())
        # print(output)

        return('Salam_35')


if __name__ == '__main__':
    app.run(debug=True)
