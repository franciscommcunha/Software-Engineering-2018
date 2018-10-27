# -*- coding: utf-8 -*-
import psycopg2
import config
import sys
import time
from random import randint
import logging

#CONSTANTS AND INITIAL VALUES
## intervalo de atualização (segundos)
INTERVALO_DE_TEMPO = 1

PERC_TEMPO_HA_MOVIM = 5

HOUR_MAX = 24
HOUR_MIN = 0

DIVISOES = ['cozinha', 'sala', 'quarto1', 'quarto2']

def main(argv):
    logging.basicConfig(filename='domotics.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info('Running addMovementData.py')
    divisoes = DIVISOES
    hour = 0

    while True:
        hour = hour + 1
        if hour == 24:
            hour = 0
        logging.info('Hour = {}'.format(hour))

        movimento = []
        for divisao in divisoes:
            movimento.append([divisao, False])

        movimento = calcMovimento(movimento)
        
        for a,b in movimento:
            if b == True:
                insertMovementData(a, hour)
                print "Movement was inserted!"

        time.sleep(INTERVALO_DE_TEMPO)


''' DATA '''
def calcMovimento(movimento):
    i = 0
    for a,b in movimento:
        rand = (randint(0, 100))
        if rand < PERC_TEMPO_HA_MOVIM:
            b = True
            movimento[i] = [a,b]
        i += 1

    return movimento

''' DATABASE '''
def insertMovementData(local, hour):
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	sql = """INSERT INTO movement(local, hour) VALUES (%s, %s)"""
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()
		print "Connected to domotics!"

		cursor.execute(sql,(local, hour))
		conn.commit()
		cursor.close()
        logging.info('Movement data to database')
	except (Exception, psycopg2.DatabaseError) as error:
        logging.error('Can\'t write movement data to database: {}'.format(error))
		print(error)
	finally:
		if conn is not None:
			conn.close()

if __name__ == "__main__":
    main(sys.argv)
