#!/usr/bin/env python
import pika, sys, os
import mysql-connector

connection = pika.BlockingConnection( pika.ConnectionParameters(host='rabbitmq server ip address'))
channel = connection.channel()
channel.exchange_declare(exchange='DatabaseExch', exchange_type='direct')
channel.queue_declare(queue='DBServerqueue', exclusive=True)
channel.queue_bind(exchange='DatabaseExch', queue='DBServerQueue')

def on_request(ch, method, props, body):
    rabbitMSG = body
    //rabbitMSG is going to come as a dictionary like this: rabbitMSG = { 'query': 'some sql statement', 'params' : 'the>
    print(rabbitMSG) 
    rabbitResponse = "goodbye from db"  //HERE is where you would replace this string after initial test and put a call >
    frontendReturn = rabbitResponse
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(frontendReturn))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='DBServerqueue', on_message_callback=on_request)

print("Waiting for BackEnd Requests")
channel.start_consuming()

def executeSQL(query,parameters):
        mydb = mysql.connector.connect(
        host="localhost",
        user="fp77",
        password="Au7K1a6cxFdj6MJ4",
        database="fp77"
        )

mycursor = mydb.cursor()

mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)

