from frontendClient import backendClient
import pika
import flask
from flask import Flask, url_for, redirect, render_template, request
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
		#return redirect('/home', code=302)
		#
		dbchk = backendClient()
		loginfo = dbchk.call({'type':'login', 'email':logemail, 'password':logpass})
		#right now just returns whether successful or not
		loginStatus = loginfo.get('result')
		#return redirect('/home', code=302)
		#
		#return redirect('/home', code=302)
		return flask.render_template("login.html", loginStatus)
	else:
		return flask.render_template('login.html')

#TODO change to function that redirects if not logged in, and asks them to login first
@app.route('/home')
def home():
    return flask.render_template("home.html")

#TODO function that if register.submit is pressed and db comes back true, redirect to home
@app.route('/register')
def register():
    return flask.render_template("register.html")

#TODO add function for recipe search





if __name__ == "__main__":
    app.run()

