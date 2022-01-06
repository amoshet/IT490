#!/usr/bin/env python
import pika
import uuid
import simplejson as json

credentials = pika.PlainCredentials('admin', 'Group2mq')
connection = pika.BlockingConnection( pika.ConnectionParameters(host='34.72.76.159' , 5672 ,'IT490',credentials))

class databaseClient(object):

	def __init__(self):
		self.connection = pika.BlockingConnection(
			pika.ConnectionParameters(host='34.72.76.159'))

		self.channel = self.connection.channel()

		result = self.channel.queue_declare(queue='', exclusive=True)
		self.callback_queue = result.method.queue

		self.channel.basic_consume(
			queue=self.callback_queue,
			on_message_callback=self.on_response,
			auto_ack=True)

	def on_response(self, ch, method, props, body):
		if self.corr_id == props.correlation_id:
			self.response = body

	def call(self, databaseMessage):
		self.response = None
		self.corr_id = str(uuid.uuid4())
		self.channel.basic_publish(
			exchange='DatabaseExch',
			routing_key='DBqueue',
			properties=pika.BasicProperties(
				reply_to=self.callback_queue,
				correlation_id=self.corr_id,
			),
			body=str(databaseMessage))
		while self.response is None:
			self.connection.process_data_events()
		return int(self.response)


databaseRPC = databaseClient()

print("Sending over Database Exchange and queue")
response = databaseRPC.call(databaseMessage) # HERE REPLACE "hello" with a variable, this variable will be what you are sending right now it is n
print(" [.] Got %r" % response)
