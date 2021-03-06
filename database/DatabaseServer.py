#!/usr/bin/env python3.8
import mysql.connector
import simplejson as json
import pika, sys, os

credentials = pika.PlainCredentials('test', 'test')
connection = pika.BlockingConnection(pika.ConnectionParameters('34.72.76.159',5672,'IT490',credentials))
channel = connection.channel()
channel.exchange_declare(exchange='DatabaseExch', exchange_type='direct')
channel.queue_declare(queue='DBServerQueue', exclusive=True)
channel.queue_bind(exchange='DatabaseExch', queue='DBServerQueue')

def executeSQL(query, parameters):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="it490",
        database="fp77"
        )

        mycursor = mydb.cursor()
        mycursor.execute(query, parameters)
        print (mycursor)
        #myresult = mycursor.fetchall()
        for row in mycursor:
                return (row[1])

        mydb.commit()

def on_request(ch, method, props, body):
        rabbitMSG = json.loads(body.decode('utf8'))
        print(rabbitMSG)
        rabbitResponse = executeSQL(rabbitMSG.get('query'), rabbitMSG.get('parameters'))
        forJSON  = rabbitResponse
        frontendReturn = json.JSONEncoder().encode(forJSON)
        ch.basic_publish(exchange='',
                routing_key=props.reply_to,
                properties=pika.BasicProperties(correlation_id = \
                        props.correlation_id),
                body=frontendReturn)
        ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='DBServerQueue', on_message_callback=on_request)

print("Waiting for Database Requests")
channel.start_consuming()
