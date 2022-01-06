#! /usr/bin/python3
from flask import Flask, request, redirect, session, url_for #response not working here

app = Flask(__name__)

@app.route('/')
def default():
    return flask.render_template("index.html")

@app.route('/index.html')
def index():
    return flask.render_template("index.html")

@app.route('/login.html')
def login():
    return flask.render_template("login.html")

if __name__ == "__main__":
    app.run()
