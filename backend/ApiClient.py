#!/usr/bin/env python
import pika
import uuid

credentials = pika.PlainCredentials('admin', 'Group2mq')
parameters = pika.ConnectionParameters('34.72.76.159' , 
                                         5672 ,
                                        'IT490', 
                                         credentials)
class apiClient(object):

	def __init__(self):
		self.connection = pika.BlockingConnection(
			pika.ConnectionParameters(host='localhost'))

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

	def call(self, apiInfo):
		self.response = None
		self.corr_id = str(uuid.uuid4())
		self.channel.basic_publish(
			exchange='APIExch',
			routing_key='APIqueue',
			properties=pika.BasicProperties(
				reply_to=self.callback_queue,
 				correlation_id=self.corr_id,
			),
			body=str(apiInfo))
		while self.response is None:
			self.connection.process_data_events()
		return int(self.response)


apiRPC = apiClient()

print("Sending over API Exchange and queue")
response = apiRPC.call("hello")  HERE REPLACE "hello" with a variable, this variable will be what you are sending right now it is n
print(" [.] Got %r" % response)
