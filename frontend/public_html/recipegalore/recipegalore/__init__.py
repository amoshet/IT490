import flask
from flask import Flask, url_for
app = Flask(__name__)

@app.route("/")
def default():
    return flask.render_template("index.html")

@app.route('/index')
def index():
    return flask.render_template("index.html")

#TODO function that if register.submit is pressed and db comes back true, redirect to home
@app.route('/login')
def login():
    return flask.render_template("login.html")

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

