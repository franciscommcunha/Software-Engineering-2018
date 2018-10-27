
from simulators import *
import sys
import logging

loggerMain = logging.getLogger('consumer.postgresqlQuery')
loggerMain.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('domoticsConsumer.log')
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
loggerMain
SIMKIND = ['temperature', 'co2', 'humidity', 'energy', 'movement']

def main(argv):

	server = "kafka:9092"

	if len(argv) < 2:
		logger.error("Not enough arguments in simulator")
		sys.exit("Not enough arguments in simulator")

	if len(argv) == 3:
		if argv[2] == "-vm":
			server = "deti-engsoft-01.ua.pt:9092"
		else:
			server = argv[2]

		simArgs = argv[3:]
	elif len(argv) == 2:
		simArgs = argv[2:]



	if len(simArgs) == 0:
		if argv[1] == 'energy':
			simArgs = APARELHOS
		else:
			simArgs = DIVISOES

	simulators = []

	if argv[1] == 'energy':
		for division in simArgs:
			sim = SimulatorType2(argv[1], division, calcEnergia, INTERVALO_DE_TEMPO[1], 0, server)
			sim.start()
			logger.info("Energy simulator initiated for appliance %s" % division)
			simulators.append(sim)
	else:
		for division in simArgs:
			if argv[1] == 'temperature':
				sim = Simulator(argv[1], division, calcTemperatura, INTERVALO_DE_TEMPO[0], TEMPERATURA_INICIAL, server)
			elif argv[1] == 'co2':
				sim = Simulator(argv[1], division, calcCO2, INTERVALO_DE_TEMPO[0], CO2_INICIAL, server)
			elif argv[1] == 'humidity':
				sim = Simulator(argv[1], division, calcHumidade, INTERVALO_DE_TEMPO[0], HUMIDADE_INICIAL, server)
			else:
				sim = MovementSimulator(argv[1], division, None, INTERVALO_DE_TEMPO[0], 0, server)
			sim.start()
			simulators.append(sim)
			logger.info("%s simulator initiated for room %s" % (argv[1],division))

	for thread in simulators:
		thread.join()

	logger.info("Exit simulator %s" % argv[1])


if __name__ == "__main__":
	main(sys.argv)

