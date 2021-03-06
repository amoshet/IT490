#!/usr/bin/python3.8
import pika
import uuid
import simplejson as json

class backendClient(object):

	def __init__(self):
		credentials = pika.PlainCredentials('test', 'test')
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('34.72.76.159',5672,'IT490',credentials))
		print("connecting to server")
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

	def call(self, flaskData):
		self.response = None
		self.corr_id = str(uuid.uuid4())
		self.channel.basic_publish(exchange='BackEndExch',routing_key='BEServerQueue', properties=pika.BasicProperties(reply_to=self.callback_queue,correlation_id=self.corr_id,),
		body= json.dumps(flaskData))
		while self.response is None:
        		self.connection.process_data_events()
		return (self.response)


#backendRPC = backendClient()

#print("Sending over Backend Exchange and queue")
#response = backendRPC.call("hello")  
#print(" [.] Got %r" % response)

