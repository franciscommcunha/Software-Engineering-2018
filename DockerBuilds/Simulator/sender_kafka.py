# http://kafka-python.readthedocs.io/en/master/usage.html
# https://github.com/dpkp/kafka-python
# https://www.youtube.com/watch?v=Ejh8UU1MrLk&t=77s

from kafka import KafkaProducer

def keyserializer(key):
	return key.encode()

def send(msgBody, key, topicName, server="kafka:9092" ):
	producer = KafkaProducer(bootstrap_servers=server, key_serializer=keyserializer) # send to
		
	string_to_bytes = str(msgBody).encode() # convert a string to bytes
	producer.send(topicName, key=key, value=string_to_bytes) # args = topic, message
	
	producer.close()



