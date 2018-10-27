# http://kafka-python.readthedocs.io/en/master/usage.html
# https://github.com/dpkp/kafka-python
# https://www.youtube.com/watch?v=Ejh8UU1MrLk&t=77s

from kafka import KafkaProducer
import logging 

logger = logging.getLogger('consumerMain.sender')
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler('domoticsConsumer.log')
fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


def keyserializer(key):
	return key.encode()

def keydeserializer(key):
    if key is not None:
        return key.decode()
    return None

def send(msgBody, key, topicName, server="kafka:9092" ):
	producer = KafkaProducer(bootstrap_servers=server, key_serializer=keyserializer) # send to
		
	string_to_bytes = str(msgBody).encode() # convert a string to bytes
	try:
		logger.debug("Consumer, before sending to kafka")
		producer.send(topicName, key=key, value=string_to_bytes) # args = topic, message
	except Exception:
		logger.error("Unable to send. Motives: timeout, kafka not started")

	finally:
		producer.close()



