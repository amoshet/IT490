#! /usr/bin/python3
import flask
from flask import request, Response, redirect, session

app = flask(__name__)

@app.route('/')
def hello():
	return flask.render
