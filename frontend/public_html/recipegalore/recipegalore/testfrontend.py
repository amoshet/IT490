from frontendClient import backendClient
import pika
import flask
from flask import Flask, url_for, redirect, render_template, request, flash

#this line is only for this test environment
app = Flask(__name__)
app.secret_key = 'shh'

@app.route("/")
def default():
	return flask.render_template("index.html")

@app.route('/index')
def index():
	return flask.render_template("index.html")

#TODO function that if register.submit is pressed and db comes back true, redirect to home
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		logemail = request.form['email']
		logpass = request.form['password']
		dbchk = backendClient()
		#sends login info to backend/db
		loginfo = dbchk.call({'type':'login', 'email':logemail, 'password':logpass})
		#right now just returns whether successful or not
		#TODO have it redirect to home and spit out the email
		# +  saying welcome to the website
		loginStatus = loginfo.get('result')
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
		#TODO redirect to register again, but tell user passwords 
		# + do not match
		if regpass2 != regpass:
			flash('Passwords do not match, please try again')
			return redirect('/register', code=302)
		dbchk2 = backendClient()
		#sends register info to backend/db
		reginfo = dbchk2.call({'type':'register', 'email':regemail, 'password':regpass})
		#right now just returns whether successful or not
		#TODO have it redirect to login and say register successful
                #TODO please login
		regStatus = reginfo.get('result')
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
#TODO change to function that redirects if not logged in, and asks them to login first
@app.route('/home')
def home():
    return flask.render_template("home.html")

#TODO add function for recipe search

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
