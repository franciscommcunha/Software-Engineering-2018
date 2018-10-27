# http://kafka-python.readthedocs.io/en/master/usage.html
# https://github.com/dpkp/kafka-python
# https://www.youtube.com/watch?v=Ejh8UU1MrLk&t=77s

from consumers import *
from memory import Memory
import sys, logging

loggerMain = logging.getLogger('consumerMain')
loggerMain.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler('domoticsConsumer.log')
fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
loggerMain.addHandler(fh)
loggerMain.addHandler(ch)


def main(argv):

	## Normal Server
	server = "kafka:9092"

	if len(argv) > 1 and argv[1] == "-debug":
		logger.setLevel(logging.DEBUG)
		loggerMain.setLevel(logging.DEBUG)
		ch2 = logging.StreamHandler()
		ch2.setLevel(logging.DEBUG)
		ch2.setFormatter(formatter)
		loggerMain.addHandler(ch2)

	if len(argv) > 1 and argv[1] == "-vm":
		server = "deti-engsoft-01.ua.pt:9092"

	if len(argv) > 2 and argv[2] == "-vm":
		server = "deti-engsoft-01.ua.pt:9092"
	else:
		if len(argv) > 2:
			server = argv[2]

	sensorList = {'temperature': consume_temperature,
					 'co2':consume_co2,
					  'humidity': consume_humidity,
					   'movement': consume_movement,
						'energy': consume_energy,
						'lights': consume_lights}
	
	consumerThreads = []

	loggerMain.info("Starting Domotics Consumers")

	consumerMem = Memory()

	try:
		for simType, funCallable in sensorList.items():
			consumer = None
			if simType == "movement":
				#continue
				#consumer = SimpleConsumer('SensorsValues', simType, 'kafka:9092', funCallable)
				consumer = MovementConsumer("SensorsValues", "ConsumerOrders", server, consumerMem)
			elif simType == "lights":
				consumer = LightsConsumer("SensorsValues", server, consumerMem)
			else:
				#continue
				consumer = SimpleConsumer('SensorsValues', simType, server, funCallable)
			consumerThreads.append(consumer)
			consumer.start()
			logger.debug("Started consumer of %s" % simType)

		loggerMain.info("Domotics Consumers Success!!!")	
		while True:
			time.sleep(1)

	except KeyboardInterrupt:
		loggerMain.info("KeybordInterrupt: Killing all Consumer threads.")
		for thread in consumerThreads:
			thead.orderToKill()

	except:
		loggerMain.info("Unknown ERROR: Killing all Consumer threads.")
		for thread in consumerThreads:
			thead.orderToKill()

	finally:
		loggerMain.info("Waiting for allConsumers threads to finish.")
		for thread in consumerThreads:
			thread.join()

	loggerMain.info("Shutdown Consumer")


if __name__ == "__main__":
	main(sys.argv)