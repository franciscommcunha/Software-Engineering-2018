# http://kafka-python.readthedocs.io/en/master/usage.html
# https://github.com/dpkp/kafka-python
# https://www.youtube.com/watch?v=Ejh8UU1MrLk&t=77s

import threading, time
import multiprocessing
from kafka import KafkaProducer

def send(msgBody):
		producer = KafkaProducer(bootstrap_servers='localhost:9092') # send to
		
		string_to_bytes = str(msgBody).encode() # convert a string to bytes
		producer.send('simulator', string_to_bytes) # args = topic, message

		producer.close()
