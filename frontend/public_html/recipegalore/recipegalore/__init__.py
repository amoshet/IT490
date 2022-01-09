from frontendClient import backendClient
import pika
import flask
from flask import Flask, url_for, redirect, render_template, request, flash
#import sys
#sys.path.insert(0, '/home/ahmed_moshet/IT490/frontend/public_html/recipegalore/recipegalore/')
#import frontendclient


app = Flask(__name__)

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
		return flask.render_template("login.html", loginStatus)
	else:
		return flask.render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		regemail = request.form['email']
		regpass = request.form['p1']
		regpass2 = request.form['p2']
		#makes sure passwords match when registering user
		#TODO redirect to register again, but tell user passwords 
		# + do not match
		if regpass2 != regpass:
			return redirect('/index', code=302)
		dbchk2 = backendClient()
		#sends register info to backend/db
		reginfo = dbchk2.call({'type':'register', 'email':regemail, 'password':regpass})
		#right now just returns whether successful or not
		#TODO have it redirect to login and say register successful
                #TODO please login
		regStatus = reginfo.get('result')
		return flask.render_template("register.html", regStatus)
	else:
		return flask.render_template('register.html')
#TODO change to function that redirects if not logged in, and asks them to login first
@app.route('/home')
def home():
    return flask.render_template("home.html")

#TODO add function for recipe search

if __name__ == "__main__":
    app.run()

