import pika


def send(msgbody):
	connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
	channel = connection.channel()

	channel.queue_declare(queue='simulator')

	channel.basic_publish(exchange='',
	                      routing_key='simulator',
	                      body=msgbody)
	print(" [x] Sent '%d'", msgbody)

	connection.close()