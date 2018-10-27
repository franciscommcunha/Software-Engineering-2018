import sys
from actuator import *


loggerMain = logging.getLogger('actuatorMain')
loggerMain.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler('domoticsActuators.log')
fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
loggerMain.addHandler(fh)
loggerMain.addHandler(ch)


DIVISIONS = ['cozinha', 'sala', 'quarto1', 'quarto2']
ACTUATORS = ["lights"]

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
	
	if len(argv) == 2 and argv[1] == "-vm":
		if argv[1] == "-vm":
			server = "deti-engsoft-01.ua.pt:9092"
		else:
			server = argv[1]

	if len(argv) > 2 and argv[2] == "-vm":
		server = "deti-engsoft-01.ua.pt:9092"

	actuatorsThreads = []
	try:
		loggerMain.info("Starting all Actuator threads.")
		for actuator in ACTUATORS: 
			for room in DIVISIONS:
				actuator = LightsActuator("ConsumerOrders", "SensorsValues", room, server)
				actuatorsThreads.append(actuator)
				loggerMain.debug("Starting Actuator of %s in romm %s." % (actuator, room))
				actuator.start()

		loggerMain.info("Domotics Actuator Success!!!")
		while True:
			time.sleep(1)

	except KeyboardInterrupt:
		loggerMain.info("KeybordInterrupt: Killing all Actuator threads.")
		for actuator in actuatorsThreads:
			actuator.orderToKill()
			loggerMain.debug("Killing Actuator of %s in room %s." % (actuator.autoController.getTye(), actuator.room))

	except:
		loggerMain.error("Unknown ERROR: Killing all Actuator threads.")
		for actuator in actuatorsThreads:
			actuator.orderToKill()
			loggerMain.debug("Killing Actuator of %s in room %s." % (actuator.autoController.getTye(), actuator.room))

	finally:
		loggerMain.info("Waiting for all Actuators threads to finish.")
		for actuator in actuatorsThreads:
			actuator.join()


if __name__ == "__main__":
	main(sys.argv)