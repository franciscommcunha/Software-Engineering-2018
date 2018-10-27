import psycopg2
import config
import sys

def main(argv):
	createEventTable()

def creatEventTable():
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	print "Connecting to database\n ->%s" %(connection)

	commands = ("""CREATE TABLE event (ID serial primary key, name varchar(30), eventDate datetime)""")

	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()

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

if __name__ == "__main__":
	main(sys.argv)