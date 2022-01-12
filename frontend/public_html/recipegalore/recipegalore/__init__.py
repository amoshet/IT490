from frontendClient import backendClient
import pika
import flask
from flask import Flask, url_for, redirect, render_template, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

@app.route("/")
def default():
	return flask.render_template("index.html")

@app.route('/index')
def index():
	return flask.render_template("index.html")

@app.route('/home')
def home():
        return flask.render_template("home.html")


@app.route('/search')
def search():
        return flask.render_template("search.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		logemail = request.form['email']
		logpass = request.form['password']
		print(logpass)
		dbchk = backendClient()
		#sends login info to backend/db
		loginfo = dbchk.call({'type':'login', 'email':logemail, 'password':logpass}).decode()
		#right now just returns whether successful or not
		#TODO have it redirect to home and spit out the email
		# +  saying welcome to the website
		loginStatus = loginfo.strip('\"')
		print(loginStatus)
		if loginStatus == 'Login Success!':
			flash('Login successful, Welcome back!')
			return redirect('/home', code=302)
		elif loginStatus == 'Login failed!':
			flash('Incorrect credentials, please try again')
			return redirect('/login', code=302)
		else:
			flash('Unknown error, please try again')
			return redirect('/login', code=302)
	else:
		return flask.render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	if request.method == 'POST':
		regemail = request.form['email']
		regpass = request.form['p1']
		regpass2 = request.form['p2']
		#makes sure passwords match when registering user
		if regpass2 != regpass:
			flash('Passwords do not match, please try again')
			return redirect('/register', code=302)
		dbchk2 = backendClient()
		#sends register info to backend/db
		reginfo = dbchk2.call({'type':'register', 'email':regemail, 'password':regpass}).decode()
		#register function checks if db added user successfully
		regStatus = reginfo.strip('\"')
		print(regStatus)
		if regStatus == 'Registration Complete':
			flash('Registration successful, Please login for the first time')
			return redirect('/login', code=302)
		elif regStatus == 'Registration Failed':
			flash('Email already in use, please login with your account, or create a new one')
			return redirect('/register', code=302)
		else:
			flash('Unknown error, please try again')
			return redirect('/register', code=302)
	else:
		return flask.render_template('register.html')

if __name__ == "__main__":
    app.run()
