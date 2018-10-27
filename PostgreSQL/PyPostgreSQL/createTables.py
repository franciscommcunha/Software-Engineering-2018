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

def main(argv):
	logging.basicConfig(filename='domotics.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
	logging.info('Running createTables.py')
	createTables()

def createTables():
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	print ("Connecting to database\n ->%s" %(connection)
	logging.info('Connecting to database -> {}'.format(connection))

	commands = (
		"""CREATE TABLE temperature (ID serial PRIMARY KEY,
									room varchar(30),
									value int,
									hour varchar(30))""",
		"""CREATE TABLE CO2 (ID serial PRIMARY KEY,
									room varchar(30),
									value int,
									hour varchar(30))""",
		"""CREATE TABLE humidity (ID serial PRIMARY KEY,
								room varchar(30),
								value int,
								hour varchar(30))""",
		"""CREATE TABLE luminosity (ID serial PRIMARY KEY,
									room varchar(30),
									value int,
									hour varchar(30))""",
		"""CREATE TABLE energy(ID serial PRIMARY KEY,
								appliance varchar(30),
								value int,
								hour varchar(30))""",
		"""CREATE TABLE movement(ID serial PRIMARY KEY,
								local varchar(30),
								hour varchar(30))""",
		"""CREATE TABLE event(ID serial PRIMARY KEY,
								name varchar(30),
								eventDate date,
								location varchar(30))""")

	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()
		print "Connected to domotics!"
		logging.info('Connected to domotics')

		for command in commands:
			cursor.execute(command)

		print "Tables were created!"
		logging.info('Tables were created')

		cursor.close()
		conn.commit()
	except(Exception, psycopg2.DatabaseError) as error:
		logging.error('Database exception: {}'.format(error))
		print(error)
	finally:
		if conn is not None:
			conn.close()

if __name__ == "__main__":
    main(sys.argv)
