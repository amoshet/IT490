import flask
from flask import Flask
app = Flask(__name__)

@app.route("/")
def default():
    return flask.render_template("index.html")

@app.route('/index.html')
def index():
    return flask.render_template("index.html")

@app.route('/login.html')
def login():
    return flask.render_template("login.html")

#TODO change to function that redirects if not logged in
@app.route('/home.html')
def home():
    return flask.render_template("home.html")

@app.route('/register.html')
def register():
    return flask.render_template("register.html")

#TODO add function for recipe search





if __name__ == "__main__":
    app.run()

