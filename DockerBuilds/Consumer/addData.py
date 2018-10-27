import psycopg2
import sys, time, logging
from random import randint

''' DATABASE '''
connection = "host = 'postgres' port = '5432' dbname = 'domotics' user = 'postgres' password = 'secret'"
#connection = "host = 'deti-engsoft-01.ua.pt' port = '5555' dbname = 'domotics' user = 'postgres' password = 'secret'"

logger = logging.getLogger('consumer.postgresqlQuery')
logger.setLevel(logging.DEBUG)
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
logger.addHandler(fh)
logger.addHandler(ch)

def insertTemperatureData(room, value, hour):
	sql = """INSERT INTO temperature(room, value, hour) VALUES(%s,%s,%s)"""
	
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()

		cursor.execute(sql,(room, value, hour,))

		conn.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		logger.error(error)
	finally:
		if conn is not None:
			conn.close()

def insertCO2Data(room, value, hour):
	sql = """INSERT INTO CO2(room, value, hour) VALUES(%s,%s,%s)"""
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()

		cursor.execute(sql,(room, value, hour))

		conn.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		logger.error(error)
	finally:
		if conn is not None:
			conn.close()

def insertHumidityData(room, value, hour):
	sql = """INSERT INTO humidity(room, value, hour) VALUES(%s, %s,%s)"""
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()

		cursor.execute(sql,(room, value, hour))

		conn.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		logger.error(error)
	finally:
		if conn is not None:
			conn.close()

def insertMovementData(local, hour):
	#connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	sql = """INSERT INTO movement(local, hour) VALUES (%s,%s)"""
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()
		print ("Connected to domotics!")

		cursor.execute(sql,(local, hour))
		conn.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		logger.error(error)
	finally:
		if conn is not None:
			conn.close()

def insertEnergyData(appliance,value, hour):
	#connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	sql = """INSERT INTO energy(appliance,value, hour) VALUES(%s,%s, %s)"""
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()
		print("Connected to domotics!")

		cursor.execute(sql,(appliance,value, hour))
		conn.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		logger.error(error)
	finally:
		if conn is not None:
			conn.close()

def insertLightsData(room, value, hour):
	#connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	sql = """INSERT INTO luminosity(room,value, hour) VALUES(%s,%s, %s)"""
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()
		print("Connected to domotics!")

		cursor.execute(sql,(room,value, hour))
		conn.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		logger.error(error)
	finally:
		if conn is not None:
			conn.close()
#if __name__ == "__main__":
#    main(sys.argv)