import psycopg2
import config
import sys
import pprint

def main(argv):

	print 'show temperature table'
	selectTemperatureData()

	print 'show C02 table'
	selectCO2Data()

	print 'show humidity table'
	selectHumidityData()

	print 'show energy table'
	selectEnergyData()

	print 'show movement table'
	selectMovementData()



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

if __name__ == "__main__":
    main(sys.argv)