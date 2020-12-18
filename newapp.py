from flask import *
import datetime, json, time, requests
import firebase_admin
from firebase_admin import firestore, credentials, auth, initialize_app
import os
from forms import RegistrationForm, LoginForm, AddProblemForm
from runcode import runcode
from pathlib import Path
from os import *
app = Flask(__name__)
# app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# db = SQLAlchemy()

app.secret_key = os.urandom(24)


cred = credentials.Certificate('new-oj-test-firebase-adminsdk-p0yb3-c8a0420853.json')
firebase_admin.initialize_app(cred, {
	'databaseURL': 'https://new-oj-test.firebaseio.com/'
})
db = firestore.client()

@app.route("/")
@app.route("/home")
def home():
	# print("print current user "+ current_user)
	# last_data=db.collection(u'problems').order_by('added_at').limit(1).get()
	# print(last_data)
	# print("printed last data ---------------------")
	all_problems = db.collection(u'problems')
	docs = all_problems.stream()
	# print(docs)
	posts=[]
	for doc in docs:
		# print(f'{doc.id} => {doc.to_dict()}')
		now_dict=doc.to_dict()
		# print(now_dict)
		# print("-------------------------------")
		statement =now_dict["statement"]
		# replace("\n","<br>")
		# print(statement)
		# 
		posts.append(now_dict)
		
	return render_template('home.html',posts=posts)

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if request.method == "POST":
		username=form.username.data
		email=form.email.data
		password=form.password.data
		# print(username)
		# print(email)
		# print(password)

		
		try:
			user = auth.get_user_by_email(email)
			flash(f'''Already registered with this email''', 'danger')
			return render_template('register.html',form=form)
		except:
			pass

		userInfo = db.collection('profiles').document(username).get()

		if userInfo.exists:
			flash(f'''Already registered with this username''', 'danger')
			return render_template('register.html')
			
		user = auth.create_user(
			email=email,
			email_verified=False,
			password=password,
			display_name=username,
			photo_url='https://picsum.photos/400',
			disabled=False)
		print('Sucessfully created new user: {0}'.format(user.uid))


		# link = auth.generate_email_verification_link(email)
		# # Construct email from a template embedding the link, and send
		# # using a custom SMTP server.
		# send_custom_email(email, link)

		db.collection('profiles').document(username).set({
			'username' : username,
			'email' : email,
		})
		return redirect(url_for('home'))
	return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == "POST":
		email=form.email.data
		password=form.password.data
		try:
			user = auth.get_user_by_email(email)
			# set the session
			user_id = user.uid
			user_email = email

			session["usr"] = user_id
			session["email"] = user_email
			session["username"]=user.display_name
			# print(session['email'])



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
	em=session['email']
	session.clear()
	flash(f'Good bye { em }!','success')
	return redirect("/");


@app.route("/comming_contest")
def comming_contest():
	return render_template('contests.html')
@app.route("/profile")
def profile():
	return render_template('profile.html')


@app.route("/addProblems", methods=['GET', 'POST'])
def addProblems():
	form=AddProblemForm()

	if request.method=="POST":
		name=form.name.data
		statement=form.statement.data
		sampleInput=form.sample_input.data
		sampleOutput=form.sample_output.data
		
		
		email ='salam35ruet17@gmail.com'

		user=auth.get_user_by_email(email)
		
		# print(format(user.display_name))
		# print(name)
		# print(statement)
		# print(sampleInput)
		# print(sampleOutput)
		# print("changed statement ")
		statement.replace('\n','<br>')
		# print('changed',statement);
		all_problems = db.collection(u'problems')
		docs = all_problems.stream()

		id=1
		for doc in docs:
			id=id+1
		# Path("E:/Projects/RUETCMS/test cases/").mkdir(parents=True, exist_ok=True)

		data={
			'name': name,
			'statement': statement,
			'input':sampleInput,
			'output':sampleOutput,
			'author':format(user.display_name),
			'time':1,
			'id':id
		}
		stid=str(id)

		os.path.join('E:/Projects/RUETCMS/test cases/', stid)

		db.collection('problems').document(stid).set(data)
		flash(f'Your problem {name} has been added','success')
		return redirect(url_for('home'))
		
	return render_template('addprob.html',form=form)


@app.route("/showproblem/<problem_id>")
def showproblem(problem_id):
	print(problem_id)
	problemid=str(problem_id)
	post = db.collection(u'problems').document(problemid).get()
	post = post.to_dict()
	print("printing name ====================")
	# print(post.statement)
	
	return render_template('show_problem.html',post=post)

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
		# r = requests.post(RUN_URL, data=data)
		# output=r.json()
		# print(output['run_status']['output'])
		# print(r.json())
		# print(output)

		return('Salam_35')
@app.route("/editproblem/<problem_id>",methods=['GET', 'POST'])
def editproblem(problem_id):
	print(problem_id)
	form=AddProblemForm()
	problemid=str(problem_id)
	post = db.collection(u'problems').document(problemid).get()
	post = post.to_dict()
	print(post)

	if request.method=="POST":
		name=request.form["name"]
		statement=request.form["statement"]
		Input=request.form["input"]
		output=request.form["output"]
		time=request.form["limit"]
		name.replace("\\n", "\n")
		data = {
			'name': name,
			'statement': statement,
			'time':time,
			'input':Input,
			'output':output
		}
		stid=str(problem_id)
		db.collection('problems').document(stid).update(data)
		flash(f'Your problem {name} has been updated','success')
		return redirect(url_for('showproblem',problem_id=problem_id))

	return render_template ('editproblem.html',form=form,post=post)


				# compilation part

from runcode import runcode

default_c_code = """#include <stdio.h>

int main(int argc, char **argv)
{
	printf("Hello C World!!\\n");
	return 0;
}    
"""

default_cpp_code = """#include <iostream>

using namespace std;

int main(int argc, char **argv)
{
	cout << "Hello C++ World" << endl;
	return 0;
}
"""

default_py_code = """import sys
import os

if __name__ == "__main__":
	print "Hello Python World!!"
"""

default_rows = "15"
default_cols = "60"

# @app.route("/runc", methods=['POST', 'GET'])
# def runc():
#     if request.method == 'POST':
#         code = request.form['code']
#         run = runcode.RunCCode(code)
#         rescompil, resrun = run.run_c_code()
#         if not resrun:
#             resrun = 'No result!'
#     else:
#         code = default_c_code
#         resrun = 'No result!'
#         rescompil = ''
#     return render_template("mainN.html",
#                            code=code,
#                            target="runc",
#                            resrun=resrun,
#                            rescomp=rescompil,
#                            rows=default_rows, cols=default_cols)

@app.route("/cpp")
@app.route("/runcpp", methods=['POST', 'GET'])
def runcpp():
	if request.method == 'POST':
		code = request.form['code']
		run = runcode.RunCppCode(code)
		rescompil, resrun = run.run_cpp_code()
		if not resrun:
			resrun = 'No result!'
	else:
		code = default_cpp_code
		resrun = 'No result!'
		rescompil = ''
	return render_template("mainN.html",
						   code=code,
						   target="runcpp",
						   resrun=resrun,
						   rescomp=rescompil,
						   rows=default_rows, cols=default_cols)

@app.route("/py")
@app.route("/runpy", methods=['POST', 'GET'])
def runpy():
	if request.method == 'POST':
		code = request.form['code']
		run = runcode.RunPyCode(code)
		rescompil, resrun = run.run_py_code()
		if not resrun:
			resrun = 'No result!'
	else:
		code = default_py_code
		resrun = 'No result!'
		rescompil = "No compilation for Python"
		
	return render_template("mainN.html",
						   code=code,
						   target="runpy",
						   resrun=resrun,
						   rescomp=rescompil,#"No compilation for Python",
						   rows=default_rows, cols=default_cols)


@app.route("/ide", methods=['POST', 'GET'])
def ide():
	if request.method == 'POST':
		code = request.form['code']
		print(request.form['solveLanguage'])
		l=request.form['solveLanguage']

		if l=="17":
			run = runcode.RunCppCode(code)
			rescompil, resrun = run.run_cpp_code()

		elif l=="11":
			run = runcode.RunCCode(code)
			rescompil, resrun = run.run_c_code()
		elif l=="2":
			run = runcode.RunPyCode(code)
			rescompil, resrun = run.run_py_code()
		
	else:
		code = default_cpp_code
		resrun = 'No result!'
		rescompil = ''
	return render_template("mainN.html",
						   code=code,
						   target="ide",
						   resrun=resrun,
						   rescomp=rescompil,
						   rows=default_rows, cols=default_cols)






























if __name__ == '__main__':
	app.run(debug=True)























































# config = {
#     "apiKey": "AIzaSyC_KXG8Vx3kD5MXDXz-dKWAYcG9xlehW6Y",
#     "authDomain": "ruetcms.firebaseapp.com",
#     "databaseURL": "https://ruetcms.firebaseio.com",
#     "projectId": "ruetcms",
#     "storageBucket": "ruetcms.appspot.com",
#     "messagingSenderId": "102610020548",
#     "appId": "1:102610020548:web:d052428fa510f293150191",
#     "measurementId": "G-XR5WZPP629"
# }
# firebase = pyrebase.initialize_app(config)
# #auth instance
# auth = firebase.auth()
# #real time database instance
# db = firebase.database();


# RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
# CLIENT_SECRET = '6eac0eba6c92665528a8c24b44781c74e3922079'

# posts = [
#     {
#         'author': 'Salam_35',
#         'title': 'Bad Story',
#         'content': 'First post content',
#         'id': '00001',
#         'date_posted': 'July 20, 2020'
#     },
#     {
#         'author': 'joynahiid',
#         'title': 'Yet Another Travelling Problem',
#         'content': 'Second post content',
#         'id':'00002',
#         'date_posted': 'July 20, 2020'
#     }
# ]


# @app.route("/")
# @app.route("/home")
# def home():
#     # print("print current user "+ current_user)
#     return render_template('home.html', posts=posts)


# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         username=form.username.data
#         email=form.email.data
#         password=form.password.data
#         print(username)
#         print(email)
#         print(password)

#         try:
#             auth.get_user_by_email(email)
#             flash(f'''Already registered with this email''', 'danger')
#             return render_template('register.html')
#         except:
#             pass

#         try:
#             cuser=db.child("user").child(username).get()
#             flash(f'''Already registered with this User Name {username}''', 'danger')
#             return render_template('register.html')
#         except:
#             pass

#         try:
#             # auth.create_user_with_email_and_password(email, password);

#             user = auth.create_user(
#             email=email,
#             email_verified=False,
#             password=password,
#             display_name=username,
#             disabled=False)
#             # user = auth.sign_in_with_email_and_password(email,password) 
#             # print(user['localId'])

#             # user['displyName']: username

#             # print("user.displyName is ")
#             # print(user.displyName)
#             # data = {
#             # "username": username,
#             # "email": email,
#             # "userid":user['localId']
#             # }
#             # db.child("users").child(username).set(data)
#             # flash(f'Account created for {form.username.data}!', 'success')
#             return redirect(url_for('home'))
#         except:
#             flash(f'Account cant be created for {form.username.data}! this email may Already in use ', 'danger')
#             return render_template('register.html', form=form)
#     return render_template('register.html', form=form)


# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if request.method == "POST":
#         email=form.email.data
#         password=form.password.data
#         try:
#             user = auth.sign_in_with_email_and_password(email, password)
#             # set the session
#             user_id = user['idToken']
#             user_email = email
#             session['usr'] = user_id
#             session["email"] = user_email

#             # print(user)

#             flash('Welcome back!', 'success')
#             return redirect(url_for('home'))
#         except:
#             flash('Login Unsuccessful. Please check username and password', 'danger')
#     else:
#         return render_template('login.html', title='Login', form=form)

# @app.route("/logout")
# def logout():   
#     print("logging out--------------------------------")
#     print(session["email"])
#     auth.current_user = None
#     #also remove the session
#     #session['usr'] = ""
#     #session["email"] = ""
#     em=session["email"]
#     session.clear()
#     flash(f'Good bye { em }!','success')
#     return redirect("/");


# @app.route("/comming_contest")
# def comming_contest():
#     return render_template('contests.html')
# @app.route("/profile")
# def profile():
#     return render_template('profile.html')


# @app.route("/addProblems", methods=['GET', 'POST'])
# def addProblems():
#     form=AddProblemForm()
#     # em=session["email"]

#     if request.method=="POST":
#         name=form.name.data
#         statement=form.statement.data
#         sampleInput=form.sample_input.data
#         sampleOutput=form.sample_output.data
#         print(name)
#         print(statement)
#         print(sampleInput)
#         print(sampleOutput)

#         # username=auth.current_user['localId']
#         # print(username)
#         user = auth.current_user['email'];
#         print(user)

#     return render_template('addprob.html',form=form)


# @app.route("/showproblem/<problem_id>")
# def showproblem(problem_id):
#     print(problem_id)
#     for x in posts:
#         if x['id']==problem_id:
#             return render_template('show_problem.html',post=x)

# @app.route("/submit_problem/<problem_id>",methods=['GET', 'POST'])
# def submit_problem(problem_id):
#     print(request.method)
#     if request.method=="POST":
#         code=request.form['source_code']
#         print(code)
#         language=request.form['solveLanguage']
#         print(request.form['solveLanguage'])
		

#         data = {
#         'client_secret': CLIENT_SECRET,
#         'async': 0,
#         'source': code,
#         'lang': "CPP14",
#         'time_limit': 5,
#         'memory_limit': 262144,
#         }



#         # print(data)
#         # r = requests.post(RUN_URL, data=data)
#         # output=r.json()
#         # print(output['run_status']['output'])
#         # print(r.json())
#         # print(output)

#         return('Salam_35')


# if __name__ == '__main__':
#     app.run(debug=True)
