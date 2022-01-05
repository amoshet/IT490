#!/usr/bin/env python
import pika, sys, os
import requests

connection = pika.BlockingConnection( pika.ConnectionParameters(host='ip of rabbitmq server'))
channel = connection.channel()
channel.exchange_declare(exchange='APIExch', exchange_type='direct')
channel.queue_declare(queue='APIServerqueue', exclusive=True)
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
channel.basic_consume(queue='APIServerqueue', on_message_callback=on_request)

print("Waiting for BackEnd Requests")
channel.start_consuming()

def test():
	variable = "goodbye"
	return variable

// add more functions that hit out to requests and return info
