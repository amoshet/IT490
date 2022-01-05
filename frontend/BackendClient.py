#!/usr/bin/env python
import pika
import uuid

class backendClient(object):

    def __init__(self):
	self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='104.197.138.105'))

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
        self.channel.basic_publish(
            exchange='BackEndExch',
            routing_key='BEServerqueue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(flaskData))
        while self.response is None:
            self.connection.process_data_events()
        return (self.response)


backendRPC = backendClient()

print("Sending over Backend Exchange and queue")
response = backendRPC.call("hello")  HERE REPLACE "hello" with a variable, this variable will be what you are sending right now it is flaskData
print(" [.] Got %r" % response)
return response
