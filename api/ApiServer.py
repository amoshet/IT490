#!/usr/bin/env python3.8
import pika, sys, os
import requests

credentials = pika.PlainCredentials('test', 'test')
connection = pika.BlockingConnection(pika.ConnectionParameters('34.72.76.159',5672,'IT490',credentials))
channel = connection.channel()
channel.exchange_declare(exchange='APIExch', exchange_type='direct')
channel.queue_declare(queue='APIServerQueue', exclusive=True)
channel.queue_bind(exchange='APIExch', queue='APIServerQueue')

def decider(type, rabbitMsg):
	return{
		'test' : lambda data : test(),
		'searchRecipes' : lambda data : searchRecipes(rabbitMsg.get('search'))

	}.get(type)(rabbitMsg)

def on_request(ch, method, props, body):
    rabbitMSG = body

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
channel.basic_consume(queue='APIServerQueue', on_message_callback=on_request)

print("Waiting for Api Requests")
channel.start_consuming()

def test():
	variable = "goodbye"
	return variable

def getAuto():
	url = "https://tasty.p.rapidapi.com/recipes/auto-complete"

	querystring = {"prefix":"chicken soup"}

	headers = {
    		'x-rapidapi-host': "tasty.p.rapidapi.com",
    		'x-rapidapi-key': "7512385757msh4aacdf9961a20c2p1225f7jsn8e19dfc61412"
    	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	print(response.text)


def getList():
	url = "https://tasty.p.rapidapi.com/recipes/list"

	querystring = {"from":"0","size":"20"}

	headers = {
		'x-rapidapi-host': "tasty.p.rapidapi.com",
		'x-rapidapi-key': "7512385757msh4aacdf9961a20c2p1225f7jsn8e19dfc61412"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	print(response.text)

def getDetail():
	url = "https://tasty.p.rapidapi.com/recipes/detail"

	querystring = {"id":"5586"}

	headers = {
		'x-rapidapi-host': "tasty.p.rapidapi.com",
		'x-rapidapi-key': "7512385757msh4aacdf9961a20c2p1225f7jsn8e19dfc61412"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	print(response.text)
#// add more functions that hit out to requests and return info
