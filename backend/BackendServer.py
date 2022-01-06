#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

def decider(type, rabbitMsg):
	return{
		'test' : lambda data : test(),
		'login' : lambda data : loginFunc(rabbitMsg.get('email'), rabbitMsg.get('password')),
#    		'allRecipes' : lambda data : allRecipes(rabbitMsq.get('search')),
#		'searchRecipes' : lambda data : searchRecipes(rabbitMsg.get('search'))

	}.get(type)(rabbitMsg)

def on_request(ch, method, props, body):
    rabbitMSG = json.loads(body.decode('utf-8'))

    print(rabbitMSG)
    rabbitResponse = decider(rabbitMSG.get('type'), rabbitMSG)
    frontendReturn = rabbitResponse
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(frontendReturn))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='BEServerQueue', on_message_callback=on_request)

print('Waiting for BackEnd Requests')
channel.start_consuming()

def test():
	variable = "goodbye"
	return variable

def loginFunc(email, password):
	try:
		SQLquery = "select Password from UserAccounts where Username=%(email)%"
		SQLparameters = {'email':email}
		DBpasser = {'query':SQLquery , 'parameters':SQLparameters}
		DBclient = databaseClient()
		DBresult = DBclient.call(DBpasser)
		if DBresult.get('message' == password):
			print("login success!")
			return True
		else:
			print("login failed!")
			return False
	except:
		print("Error in loginFunc")
def registerFunc(email, password):
	try:
		SQLquery = "insert Email and Password from UserAccounts"
		SQLparameters = {'email':email , 'password':password}
		DBpasser = {'query':SQLquery , 'parameters':SQLparameters}
		DBclient = databaseClient()
		DBresult = DBclient.call(DBpasser)
		if DBresult.get('message' == password):
			print('Registration success!')
			return True
		else:
			print('Registration failed!')
			return  False
	except:
		print("Error in registerFun")
#def allRecipes(search)
#	APIclient = apiClient()
#	apiResponse = APIclient.call({
#	'type': 'allRecipes',
#	'query' : search})
#	print(apiResponse)
#	return apiResponse

#def searchRecipes(search)
#	APIclient = apiClient()
#	apiResponse = APIclient.call({
#	'type': 'searchRecipe',
#	'query' : search})
#	print(apiResponse)
#	return apiResponse
