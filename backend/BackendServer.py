#!/usr/bin/env python
import pika, sys, os
from DatabaseClient import databaseClient
from APIClient import apiClient

connection = pika.BlockingConnection( pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='BackEndExch', exchange_type='direct')
channel.queue_declare(queue='BEServerqueue', exclusive=True)
channel.queue_bind(exchange='BackEndExch', queue='BEServerQueue')

def decider(type, rabbitMsg):
	return:
		'login' : loginFunc(rabbitMsg.get('email'), rabbitMsg.get('password'))
    		'allRecipes' : allRecipes()
		'searchRecipes' : searchRecipes(rabbitMsg.get('search'))

def on_request(ch, method, props, body):
    rabbitMSG = body

    print(rabbitMSG)
    rabbitResponse = decider(rabbitMSG.get('type'), rabbitMSG)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(rabbitResponse))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='BEServerqueue', on_message_callback=on_request)

print("Waiting for BackEnd Requests")
channel.start_consuming()


def loginFunc(email, password):
	SQLquery = "select Password from UserAccounts where Username=%(email)%"
	SQLparameters = {'email':email}
	DBpasser = {'query':SQLquery , 'parameters':SQLparameters}
	DBclient = databaseClient()
	DBresult = DBclient.call(DBpasser)
	if DBresult.get('message' = password:
		print("login success!")
		return True
	else:
		print("login failed!")
		return False
def registerFunc(email, password):
	SQLquery = "insert Email and Password from UserAccounts"
	SQLparameters = {'email':email , 'password':password}
	DBpasser = {'query':SQLquery , 'parameters':SQLparameters}
	DB client = databaseClient()
	DBresult = DBclient.call(DBpasser)
	if DBresult.
		

def allRecipes()
	APIclient = apiClient()
	apiResponse = APIclient.call({
	'type': 'allRecipes'})
	print(apiResponse)
	return apiResponse

def searchRecipes(search)
	APIclient = apiClient()
	apiResponse = APIclient.call({
	'type': 'searchRecipe',
	'query' : search})
	print(apiResponse)
	return apiResponse
