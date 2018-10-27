# http://kafka-python.readthedocs.io/en/master/usage.html
# https://github.com/dpkp/kafka-python
# https://www.youtube.com/watch?v=Ejh8UU1MrLk&t=77s

from kafka import KafkaConsumer
import json

# To consume messages 
consumer = KafkaConsumer('simulator',								                     # topic
                         group_id='domotics', 					               # group
                         bootstrap_servers=['localhost:9092'], 	       # consume from
                         auto_offset_reset='earliest', 			           # consume earliest available messages
                         enable_auto_commit=False) 				             # don't commit offsets

for message in consumer:
	bytes_to_string = message.value.decode() # if it is a string
	# bytes_to_int = int.from_bytes(message.value, byteorder='big') # if it is an integer

	print(" [x] Received {}".format(bytes_to_string))  


"""
# consume json messages
KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('ascii')))

# StopIteration if no message after 1sec
KafkaConsumer(consumer_timeout_ms=1000)
"""
