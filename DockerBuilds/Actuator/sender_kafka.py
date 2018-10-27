# http://kafka-python.readthedocs.io/en/master/usage.html
# https://github.com/dpkp/kafka-python
# https://www.youtube.com/watch?v=Ejh8UU1MrLk&t=77s

from kafka import KafkaProducer

def keyserializer(key):
	return key.encode()

def keydeserializer(key):
    if key is not None:
        return key.decode()
    return None

def send(msgBody, key, topicName , server="kafka:9092"):
	producer = KafkaProducer(bootstrap_servers=server, key_serializer=keyserializer) # send to
		
	string_to_bytes = str(msgBody).encode() # convert a string to bytes
	try:
		producer.send(topicName, key=key, value=string_to_bytes) # args = topic, message
	except Exception:
		print("Unable to send. Motives: timeout, kafka not started")

	producer.close()



