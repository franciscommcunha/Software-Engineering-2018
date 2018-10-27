from kafka import KafkaConsumer
import threading, logging, time
import addData as postgresCOM
from datetime import datetime
from states import LightsState, BasicState, MovementState
from sender_kafka import send


logger = logging.getLogger('consumerMain.consumers')
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler('domoticsConsumer.log')
fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


def consume_temperature(consumer, key):
	offset = 0
	for message in consumer:
		if message.key == key and message.offset > offset:
			logger.debug("Consumer %s received message: %s" % (key, message))
			offset = message.offset
			m = message.value.decode().split('|')
			postgresCOM.insertTemperatureData(m[0], int(m[1]), datetime.now().hour%24 )
			logger.info("Added %s data to DB for room %s" % (key, m[0]))


def consume_co2(consumer, key):
	offset = 0
	for message in consumer:
		if message.key == key and message.offset > offset:
			logger.debug("Consumer %s received message: %s" % (key, message))
			offset = message.offset
			m = message.value.decode().split('|')
			postgresCOM.insertCO2Data(m[0], int(m[1]), datetime.now().hour%24 )
			logger.info("Added %s data to DB for room %s" % (key, m[0]))


def consume_humidity(consumer, key):
	offset = 0
	for message in consumer:
		if message.key == key and message.offset > offset:
			logger.debug("Consumer %s received message: %s" % (key, message))
			offset = message.offset
			m = message.value.decode().split('|')
			postgresCOM.insertHumidityData(m[0], int(m[1]) , datetime.now().hour%24 )
			logger.info("Added %s data to DB for room %s" % (key, m[0]))


def consume_energy(consumer, key):
	offset = 0
	lista = 0
	counter = 0
	for message in consumer:
		if message.key == key and message.offset > offset:
			logger.debug("Consumer %s received message: %s" % (key, message))
			offset = message.offset
			m = message.value.decode().split('|')
			postgresCOM.insertEnergyData(m[0], int(m[1]), datetime.now().hour%24 )
			logger.info("Added %s data to DB for room %s" % (key, m[0]))


def consume_movement(consumer, key):
	offset = 0
	for message in consumer:
		logger.debug("Consumer offset: %s" % (message.offset))

		#verifies if message is handled by this consumer thread.
		logger.debug("Consumer checking if message.key is equal to his key ")
		if message.key == key and message.offset > offset:
				logger.debug("Consumer %s received message: %s" % (key, message))
				offset = message.offset
				m = message.value.decode().split('|')
				#Check if state has changed in sensor
				if int(m[1]) == 0:
					#Register the state change in database
					logger.debug("Movement as changed at %s." % (m[0]))
					postgresCOM.insertMovementData(m[0], datetime.now().hour%24)
					logger.info("Added %s data to DB for room %s" % (key, m[0]))
					break
		
	return offset


def consume_lights(consumer, key, memory):
	offset = 0
	for message in consumer:
		if message.key == key:
			logger.debug("Consumer message received and accepted: %s" % (message.value.decode()))
			m = message.value.decode().split('|')

			if not memory.hasState(key, m[0]):
				memory.addState(key, m[0], LightsState())

			if not (int(memory.getEnumState(key, m[0])) == int(m[1])):
				logger.info("Consumer: lights state changed form %d to %d" % (int(memory.getEnumState(key, m[0])), int(m[1])))
				memory.changeState(key, m[0], BasicState.ON if int(m[1]) == 0 else BasicState.OFF, m[2])
				postgresCOM.insertLightsData(m[0], int(m[1]), datetime.now().hour%24)


def consume_avd(consumer, key):
	for message in consumer:
		print("Avg: {}".format(message))


def keydeserializer(key):
	if key is not None:
		return key.decode()
	return None


class SimpleConsumer(threading.Thread):
	def __init__(self, topic, key, bootstrap_servers, callback):
		threading.Thread.__init__(self)
		self.topic = topic
		self.key = key
		self.servers = bootstrap_servers
		logger.debug("Creating consumer of %s of type %s" % (self.topic, self.key))
		self.consumer = KafkaConsumer(self.topic,
							bootstrap_servers=[self.servers],
							auto_offset_reset='latest',                
							enable_auto_commit=False,
							key_deserializer=keydeserializer)
		logger.debug("New kafkaConsumer creater for topic %s" % self.topic)
		self.callback = callback
		self.kill = False

	def run(self):
		while not self._timeToDie():
			self.callback(self.consumer, self.key)
		logger.debug("Consumer of %s of type %s is shutting down" % (self.topic, self.key))

	def orderToKill(self):
		self.kill = True
		
	def _timeToDie(self):
		return self.kill


#topicReceiver: "SensorValues"
#topicSender: "ConsumerOrders"
#keyAct : "lights"
class MovementConsumer(SimpleConsumer):
	def __init__(self, topicReceiver, topicSender, bootstrap_servers, memory):
		SimpleConsumer.__init__(self, topicReceiver, "movement", bootstrap_servers, None)
		self.topicSender = topicSender
		self.keyAct = "lights"
		self.memory = memory

	def run(self):
		offset = 0
		self.consume_movement(self.consumer, self.key, offset, self.memory)
		logger.debug("Consumer of %s of type %s is shutting down" % (self.topic, self.key))
	
	#Process and reply of new messages from broker
	def consume_movement(self, consumer, key, offset, memory):
		for message in consumer:
			#verifies if message is handled by this consumer thread.
			logger.debug("Consumer checking if message.key %s is equal to his key %s " % (message.key, key))
			if message.key == key and message.offset > offset:
				logger.debug("Consumer %s received message: %s" % (key, message))
				offset = message.offset
				m = message.value.decode().split('|')

				#Check if this kind of state exists in memory
				if not memory.hasState(key, m[0]):
					logger.debug("Consumer movement: add in memory a new State of type %s and %s" % (key, m[0]))
					memory.addState(key, m[0], MovementState())
					
				#Check if state has changed in sensor
				logger.debug("Comparing in consumer enum with message")
				if  not (int(m[1]) == int(memory.getEnumState(key, m[0]))):
					#Room m[0] has movement, check lights in that room
					if int(m[1]) == 0:

						memory.changeState(key, m[0], BasicState.ON)

						#check if lights state exists in memory
						if not memory.hasState(self.keyAct, m[0]):
							memory.addState(self.keyAct, m[0], LightsState())

						if datetime.now().hour > 18 and datetime.now().hour < 8:
							logger.debug("Consumer: before sending 1")
							#its night time, send msg to turn on lighs
							msg = "%s|%s|%s" % (m[0], str(0), "auto")
							send(msg, self.keyAct, self.topicSender, self.servers)
							logger.debug("Sent order to turn ON the lights at %s" % (m[0]))
						else:
							logger.debug("Consumer: before sending 2")
							#its day time, send msg to turn off lights
							msg = "%s|%s|%s" % (m[0], str(1), "auto")
							send(msg, self.keyAct, self.topicSender, self.servers)
							logger.info("Sent order to turn OFF the lights at %s" % (m[0]))
					#Room m[0] has no movement
					else:
						memory.changeState(key, m[0], BasicState.OFF)
						msg = "%s|%s|%s" % (m[0], 1, "auto")
						send(msg, self.keyAct, self.topicSender, self.servers)
						logger.debug("Sent order to turn OF the lights at %s because room has no movement" % (m[0]))
					#Register the state change in database
					logger.debug("Movement as changed at %s." % (m[0]))
					postgresCOM.insertMovementData(m[0], (datetime.now().hour%24) )
					logger.info("Added %s data to DB for room %s" % (key, m[0]))

			if self._timeToDie():
				break

##Consumer for lights
class LightsConsumer(SimpleConsumer):
	def __init__(self, topicReceiver, bootstrap_servers, memory):
		SimpleConsumer.__init__(self, topicReceiver, "lights", bootstrap_servers, consume_lights)
		self.memory = memory

	def run(self):
		while not self._timeToDie():
			self.callback(self.consumer, self.key, self.memory)
		logger.debug("Consumer of %s of type %s is shutting down" % (self.topic, self.key))
