''' 
Before starts python with postgreSQL, you need to access postgres. By terminal execute the next commands:
	sudo -u postgres psql postgres
		> \password postgres
		> secret
		> \q
	sudo -u postgres createdb domotics

If you want to connect to database by terminal: psql -U postgres domotics. If you receive a message like "psql: FATAL: Peer authentication failed for user "postgres", then you should edit (with sudo) the file pg_hba.conf in line "local  all  postgres  peer" to "local  all postgres md5".
After that you can enter into database.
'''

import psycopg2
import config
import sys
import logging

logging.basicConfig(filename='domotics.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def connectDatabase():
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	print "Connecting to database\n ->%s" %(connection)

	conn = psycopg2.connect(connection)
	cursor = conn.cursor()
	print "Connected to domotics!"

def createTables():
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	print "Connecting to database\n ->%s" %(connection)

	commands = (
		"""CREATE TABLE temperature (ID serial PRIMARY KEY,
									value int)""",
		"""CREATE TABLE CO2 (ID serial PRIMARY KEY,
									value int)""",
		"""CREATE TABLE humidity (ID serial PRIMARY KEY,
								value int)""",
		"""CREATE TABLE luminosity (ID serial PRIMARY KEY,
									value int)""",
		"""CREATE TABLE energy(ID serial PRIMARY KEY,
								appliance varchar(30),
								value int)""",
		"""CREATE TABLE movement(ID serial PRIMARY KEY,
								local varchar(30))""")

	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()
		print "Connected to domotics!"

		for command in commands:
			cursor.execute(command)

		print "Tables were created!"

		cursor.close()
		conn.commit()
	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def insertTemperatureData(value):
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	sql = """INSERT INTO temperature(value) VALUES(%s)"""
	
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()
		print "Connected to domotics!"

		cursor.execute(sql,[value])
		conn.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def insertCO2Data(value):
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	sql = """INSERT INTO CO2(value) VALUES(%s)"""
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()
		print "Connected to domotics!"

		cursor.execute(sql,[value])
		conn.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def insertHumidityData(value):
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	sql = """INSERT INTO humidity(value) VALUES(%s)"""
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()
		print "Connected to domotics!"

		cursor.execute(sql,[value])
		conn.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def insertLuminosityData(value):
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	sql = """INSERT INTO luminosity(value) VALUES(%s)"""
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()
		print "Connected to domotics!"

		cursor.execute(sql,(value))
		conn.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def insertEnergyData(appliance,value):
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	sql = """INSERT INTO energy(appliance,value) VALUES(%s,%s)"""
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()
		print "Connected to domotics!"

		cursor.execute(sql,(appliance,value))
		conn.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def insertMovementData(local):
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	sql = """INSERT INTO movement(local) VALUES (%s)"""
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()
		print "Connected to domotics!"

		cursor.execute(sql,[local])
		conn.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def deleteTemperatureData():
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()
		print "Connected to domotics!"

		cursor.execute("DELETE * FROM temperature")
		conn.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def deleteCO2Data():
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()
		print "Connected to domotics!"

		cursor.execute("DELETE * FROM CO2")
		conn.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def deleteHumidityData():
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()
		print "Connected to domotics!"

		cursor.execute("DELETE * FROM humidity")
		conn.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def deleteLuminosityData():
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()
		print "Connected to domotics!"

		cursor.execute("DELETE * FROM luminosity")
		conn.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def deleteEnergyData():
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()
		print "Connected to domotics!"

		cursor.execute("DELETE * FROM energy")
		conn.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def deleteMovementData():
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()
		print "Connected to domotics!"

		cursor.execute("DELETE * FROM movement")
		conn.commit()
		cursor.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


def selectTemperatureData():
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	print "Connecting to database\n ->%s" %(connection)

	conn = psycopg2.connect(connection)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM temperature")

	records = cursor.fetchall()

	pprint.pprint(records)

def selectCO2Data():
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	print "Connecting to database\n ->%s" %(connection)

	conn = psycopg2.connect(connection)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM CO2")

	records = cursor.fetchall()

	pprint.pprint(records)

def selectHumidityData():
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	print "Connecting to database\n ->%s" %(connection)

	conn = psycopg2.connect(connection)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM humidity")

	records = cursor.fetchall()

	pprint.pprint(records)

def selectLuminosityData():
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	print "Connecting to database\n ->%s" %(connection)

	conn = psycopg2.connect(connection)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM luminosity")

	records = cursor.fetchall()

	pprint.pprint(records)

def selectEnergyData():
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	print "Connecting to database\n ->%s" %(connection)

	conn = psycopg2.connect(connection)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM energy")

	records = cursor.fetchall()

	pprint.pprint(records)

def selectMovementData():
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	print "Connecting to database\n ->%s" %(connection)

	conn = psycopg2.connect(connection)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM movement")

	records = cursor.fetchall()

	pprint.pprint(records)



