# -*- coding: utf-8 -*-
import sender_kafka
from kafka import errors as Errors
import time, logging
import threading
from random import randint



logger = logging.getLogger('simMain.simulators')
logger.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

fh = logging.FileHandler('domoticsSim.log')
fh.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

################# UNIDADES #################
# temperatura       ºC
# CO2               ppm
# humidade          %
############################################

################# CONSTANTES #################

## intervalo de atualização (minutos)

EXIT_TAG = 0
INTERVALO_DE_TEMPO = [10, 60]

TEMPERATURA_MIN = 10
TEMPERATURA_MAX = 25
TEMPERATURA_INICIAL = 16

CO2_MIN = 300
CO2_MAX = 900
CO2_INICIAL = 600

HUMIDADE_MIN = 10
HUMIDADE_MAX = 90
HUMIDADE_INICIAL = 55

DIVISOES = ['cozinha', 'sala', 'quarto1', 'quarto2']
##############################################

#['aparelho', gastoPorHoraWatts, %tempoLigado]
APARELHOS = [ ['tv', 120, 0.4], ['luz_quarto', 60,  0.2], ['aquecedor', 2000, 0.15], ['frigorifico', 100, 1] ]
##############################################

## intervalo de atualização (segundos)
PERC_TEMPO_HA_MOVIM = 5

###############################################
###SIMULATOR FUNCTIONS####
def calcTemperatura(current):
	rand = (randint(-2, 2))
	if current + rand < TEMPERATURA_MIN:
		return TEMPERATURA_MIN
	elif current + rand > TEMPERATURA_MAX:
		return TEMPERATURA_MAX
	else:
		return current + rand

def calcCO2(current):
	rand = (randint(-50, 50))
	if current + rand < CO2_MIN:
		return CO2_MIN
	elif current + rand > CO2_MAX:
		return CO2_MAX
	else:
		return current + rand

def calcHumidade(current):
	rand = (randint(-5, 5))
	if current + rand < HUMIDADE_MIN:
		return HUMIDADE_MIN
	elif current + rand > HUMIDADE_MAX:
		return HUMIDADE_MAX
	else:
		return current + rand


def calcEnergia(device):
	enerySpent = device[1] * device[2]
	toReturn = [device[0], enerySpent]

	rand = (randint(0, 100))
	if rand < 50:
		device[2] = round(device[2] * 1.05, 2)
	else:
		device[2] = round(device[2] * 0.95, 2)
	if device[2] > 1:
		device[2] = 1
	elif device[2] < 0:
		device[2] = 0

	return toReturn


##Refactor
def calcMovimento(division, prevstate):
	movement = []
	rand= (randint(0, 100))
	hasMovement = 0 if rand < PERC_TEMPO_HA_MOVIM else 1
	if hasMovement == 0:
		hasMovement = 0 if prevstate == 1 else 1
	else:
		hasMovement = prevstate
	return [division, hasMovement]


###################################################
#########SIMULATOR CLASSS #########################

class Simulator(threading.Thread):
	def __init__(self, simType ,division, simFunction, sleeptime=10, defaultVal=0, server="kafka:9092"):
		threading.Thread.__init__(self)
		self.type = simType
		self.division = division
		self.sim = simFunction
		self.sleep = sleeptime
		self.value = defaultVal
		self.server = server

	def run(self):
		while(EXIT_TAG == 0):
			self.value = self.sim(self.value)
			toStore = '%s|%d' % (self.division, self.value)
			try:
				sender_kafka.send(toStore, self.type, 'SensorsValues', self.server)
				logger.debug("Data sent to Kafka broker: %s for %s value %s" % (self.type, self.division, self.value))
			except Exception:
				logger.warning("Simulator cannot send due to Kafka not operational yet!")
				time.sleep(10)
				continue
			time.sleep(self.sleep)


class SimulatorType2(Simulator):
	def __init__(self, simType ,deviceStats, simFunction, sleeptime=2, defaultVal=0, server="kafka:9092"):
		Simulator.__init__(self, simType, deviceStats, simFunction, sleeptime, defaultVal, server)
	def run(self):
		while(EXIT_TAG == 0):
			returned = self.sim(self.division)
			toStore = '%s|%d' % (returned[0], int(returned[1]))
			try:
				sender_kafka.send(toStore, self.type, 'SensorsValues', self.server)
				logger.debug("Data sent to Kafka broker: %s for %s" % (self.type, self.division[0]))
			except Exception:
				logger.warning("Simulator cannot send due to Kafka not operational yet!")
				time.sleep(10)
				continue
			time.sleep(self.sleep)


class MovementSimulator(Simulator):
	def __init__(self, simType ,deviceStats, simFunction=None, sleeptime=10, defaultVal=1, server="kafka:9092"):
		Simulator.__init__(self, simType, deviceStats, calcMovimento, sleeptime, defaultVal, server)

	def run(self):
		while(EXIT_TAG == 0):
			returned = self.sim(self.division, self.value)
			self.value = returned[1]
			toStore = '%s|%d' % (returned[0], int(returned[1]))
			try:
				sender_kafka.send(toStore, self.type, 'SensorsValues', self.server)
				logger.debug("Data sent to Kafka broker: %s for %s" % (self.type, self.division))
			except Exception:
				logger.warning("Simulator cannot send due to Kafka not operational yet!")
				time.sleep(10)
				continue
			time.sleep(self.sleep)