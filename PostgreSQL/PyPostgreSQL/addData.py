# -*- coding: utf-8 -*-
import psycopg2
import config
import sys
import time
from random import randint
import logging

''' CONSTANTS AND INITIAL VALUES'''
################# UNIDADES #################
# temperatura       ºC
# CO2               ppm
# humidade          %
############################################

################# CONSTANTES #################

## intervalo de atualização (minutos)
INTERVALO_DE_TEMPO = 0.1

TEMPERATURA_MIN = 10
TEMPERATURA_MAX = 25
TEMPERATURA_INICIAL = 16

CO2_MIN = 300
CO2_MAX = 900
CO2_INICIAL = 600

HUMIDADE_MIN = 10
HUMIDADE_MAX = 90
HUMIDADE_INICIAL = 55
LUMINOSIDADE_INICIAL=0

PERC_TEMPO_HA_MOVIM = 5

DIVISOES = ['cozinha', 'sala', 'quarto1', 'quarto2']

def main(argv):
	logging.basicConfig(filename='domotics.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
	logging.info('Running addData.py')

	rooms = DIVISOES

	atuadorTemperatura = []
	temperature = []
	co2 = []
	humidity = []
	luminosidade = []

	for x in range(0, len(DIVISOES)):
		atuadorTemperatura.append(False)
		temperature.append(TEMPERATURA_INICIAL)
		co2.append(CO2_INICIAL)
		humidity.append(HUMIDADE_INICIAL)
		luminosidade.append(LUMINOSIDADE_INICIAL)

	hour = 0

	#connectDatabase() 
	#createTables()  - verify if tables were created by typing (postgres size) \dt
	while True:
		hour = hour + 1

		if hour == 24:
			hour = 0

		logging.info('Hour = {}'.format(hour))

		temperature = calcTemperature(temperature, atuadorTemperatura)
		insertTemperatureData(temperature, rooms, hour)
		
		co2 = calcCO2(co2)
		insertCO2Data(co2, rooms, hour)
        
		humidity = calcHumidity(humidity, atuadorTemperatura)
		insertHumidityData(humidity, rooms, hour)

		imprimir(rooms, temperature, co2, humidity, luminosidade)

		time.sleep(INTERVALO_DE_TEMPO * 10)

''' DATA '''

def calcTemperature(lista, atuadorTemperatura):
	i = 0
	for x in lista:
		if atuadorTemperatura[i] == True:
			print("TRUE")
		else:
			rand = (randint(-2, 2))
			if x + rand < TEMPERATURA_MIN:
				lista[i] = TEMPERATURA_MIN
			elif x + rand > TEMPERATURA_MAX:
				lista[i] = TEMPERATURA_MAX
			else:
				lista[i] = x + rand
		i += 1
	logging.info('Temperature = {}'.format(lista))
	return lista

def calcCO2(lista):
	i = 0
	for x in lista:
		rand = (randint(-50, 50))
		if x + rand < CO2_MIN:
			lista[i] = CO2_MIN
		elif x + rand > CO2_MAX:
			lista[i] = CO2_MAX
		else:
			lista[i] = x + rand
		i += 1
		logging.info('CO2 = {}'.format(lista))
	return lista

def calcHumidity(lista, atuadorTemperatura):
	i = 0
	for x in lista:
		if atuadorTemperatura[i] == True:
			print("TRUE")
		else:
			rand = (randint(-5, 5))
			if x + rand < HUMIDADE_MIN:
				lista[i] = HUMIDADE_MIN
			elif x + rand > HUMIDADE_MAX:
				lista[i] = HUMIDADE_MAX
			else:
				lista[i] = x + rand
		i += 1
		logging.info('Humidity = {}'.format(lista))
	return lista


''' DATABASE '''
def insertTemperatureData(values, rooms, hour):
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	sql = """INSERT INTO temperature(room, value, hour) VALUES(%s,%s, %s)"""
	
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()

		i = 0
		for room in rooms:
			cursor.execute(sql,(room, values[i], hour))
			i += 1

		conn.commit()
		cursor.close()
		logging.info('Temperature values to database')
	except (Exception, psycopg2.DatabaseError) as error:
		logging.error('Can\'t write temperature values to database: {}'.format(error))
		print(error)
	finally:
		if conn is not None:
			conn.close()

def insertCO2Data(values,rooms, hour):
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	sql = """INSERT INTO CO2(room, value, hour) VALUES(%s,%s, %s)"""
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()

		i = 0
		for room in rooms:
			cursor.execute(sql, (room, values[i], hour))
			i += 1

		conn.commit()
		cursor.close()
		logging.info('CO2 values to database')
	except (Exception, psycopg2.DatabaseError) as error:
		logging.error('Can\'t write CO2 values to database: {}'.format(error))
		print(error)
	finally:
		if conn is not None:
			conn.close()

def insertHumidityData(values, rooms, hour):
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	sql = """INSERT INTO humidity(room, value, hour) VALUES(%s, %s, %s)"""
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()

		i = 0
		for room in rooms:
			cursor.execute(sql, (room, values[i], hour))
			i += 1

		conn.commit()
		cursor.close()
		logging.info('Humidity values to database')
	except (Exception, psycopg2.DatabaseError) as error:
		logging.error('Can\'t write humidity values to database: {}'.format(error))
		print(error)
	finally:
		if conn is not None:
			conn.close()


def imprimir(divisoes, temperatura, co2, humidade, luminosidade):
	i = 0
	lista = []
	for x in divisoes:
		lista.append([x, "temp:", temperatura[i], "co2:", co2[i], "hum:", humidade[i], "lum:", luminosidade[i]])
		i += 1
	print(lista)

if __name__ == "__main__":
    main(sys.argv)
