#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import codecs
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import pika, sys, os
import simplejson as json
from DatabaseClient import databaseClient
from ApiClient import apiClient

credentials = pika.PlainCredentials('test', 'test')
connection = pika.BlockingConnection(pika.ConnectionParameters('34.72.76.159',5672,'IT490',credentials))
channel = connection.channel()
channel.exchange_declare(exchange='BackEndExch', exchange_type='direct')
channel.queue_declare(queue='BEServerQueue', exclusive=True)
channel.queue_bind(exchange='BackEndExch', queue='BEServerQueue')
def tester():
        variable = {'test': "goodbye"}
        return variable

def loginFunc(email, password):
       try:
                SQLparameters = {'email':email , 'password':password}
                DBclient = databaseClient()
                DBresult = DBclient.call({'query':"SELECT Username, Password FROM login WHERE Username=%(email)s", 'parameters' : {'email' : email, 'password' : password}}).decode()
                print(DBresult)
                print(password)
                DBstatus = DBresult.strip('\"')
                if DBstatus == password:
                        print("login success!")
                        returner = "Login Success!"
                        return(returner)
                else:
                        print("login failed!")
                        returner = "Login failed!"
                        return(returner)
       except:
                print("Error in loginFunc")
                returner = "Login failed!"
                return(returner)
def registerFunc(email, password):
        try:
                SQLparameters = {'email':email , 'password':password}
                DBclient = databaseClient()
                DBresult = DBclient.call({'query': "INSERT INTO login (Username, Password) VALUE (%(email)s, %(password)s)", 'parameters' : SQLparameters})
                returner = "Registration Complete"
                return(returner)
        except:
                print("Error in registerFun")
                returner = "Registration Failed"
                return(returner)

def decider(type, rabbitMsg):
	return{
		'test' : lambda data : tester(),
		'login' : lambda data : loginFunc(rabbitMsg.get('email'), rabbitMsg.get('password')),
                'register' : lambda data: registerFunc(rabbitMsg.get('email'), rabbitMsg.get('password')),
                'getAuto' : lambda data : getAuto(rabbitMsq.get('search')),
		'getList' : lambda data : getList(rabbitMsg.get('search')),
		'getDetail' : lambda data : getDetail(rabbitMsg.get('search'))

	}.get(type)(rabbitMsg)

def on_request(ch, method, props, body):
    rabbitMSG = json.loads(body.decode('utf8'))
    print(rabbitMSG)
    rabbitResponse = decider(rabbitMSG.get('type'), rabbitMSG)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=json.dumps(rabbitResponse))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='BEServerQueue', on_message_callback=on_request)

print('Waiting for BackEnd Requests')
channel.start_consuming()


def getAuto(search):
	try:
		APIclient = apiClient()
		apiResponse = APIclient.call({
		'type': 'getAuto',
		'query' : search})
		print(apiResponse)
		return apiResponse
	except:
		print("Error in getAuto API function")
def getList(search):
	try:
		APIclient = apiClient()
		apiResponse = APIclient.call({
		'type': 'getList',
		'query' : search})
		print(apiResponse)
		return apiResponse
	except:
		print("Error in getList API function")
def getDetail(search):
	try:
		APIclient = apiClient()
		apiResponse = APIclient.call({
		'type': 'getDetail',
		'query' : search})
		print(apiResponse)
		return apiResponse
	except:
		print("Error in getDetail API funtion")
