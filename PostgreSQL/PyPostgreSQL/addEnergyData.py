import psycopg2
import config
import sys
import time
from random import randint
import logging

#CONSTANTS AND INITIAL VALUES
INTERVALO_DE_TEMPO = 3600
APARELHOS = [ ['tv', 120, 0.4], ['luz_quarto', 60,  0.2], ['aquecedor', 2000, 0.15], ['frigorifico', 100, 1] ]

def main(argv):
    logging.basicConfig(filename='domotics.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info('Running addEnergyData.py')
    aparelhos = APARELHOS
    hour = 0

    while True:
        hour = hour + 1
        if hour == 24:
            hour = 0

        logging.info('Hour = {}'.format(hour))

        gastoNaUltimaHora = []
        for aparelho in aparelhos:
            gastoNaUltimaHora.append([aparelho[0], 0])
        gastoNaUltimaHora = calcEnergia(gastoNaUltimaHora, aparelhos)

        for a,b in gastoNaUltimaHora:
           insertEnergyData(a,b,hour)
           print 'energy was inserted!'

        time.sleep(INTERVALO_DE_TEMPO)

'''DATA'''
def calcEnergia(gastoNaUltimaHora, aparelhos):
    i = 0
    for a,b in gastoNaUltimaHora:
        b = aparelhos[i][1] * aparelhos[i][2]
        gastoNaUltimaHora[i] = [a,b]

        rand = (randint(0, 100))
        if rand < 50:
            aparelhos[i][2] = round(aparelhos[i][2] * 1.05, 2)
        else:
            aparelhos[i][2] = round(aparelhos[i][2] * 0.95, 2)
        if aparelhos[i][2] > 1:
            aparelhos[i][2] = 1
        elif aparelhos[i][2] < 0:
            aparelhos[i][2] = 0

        i += 1

    return gastoNaUltimaHora

'''DATABASE '''
def insertEnergyData(appliance,value, hour):
	connection = "host = 'localhost' dbname = 'domotics' user = 'postgres' password = 'secret'"
	sql = """INSERT INTO energy(appliance,value, hour) VALUES(%s,%s,%s)"""
	conn = None
	try:
		conn = psycopg2.connect(connection)
		cursor = conn.cursor()
		print "Connected to domotics!"

		cursor.execute(sql,(appliance,value,hour))
		conn.commit()
		cursor.close()
        logging.info('Energy values to database')
	except (Exception, psycopg2.DatabaseError) as error:
        logging.error('Can\'t write energy values to database: {}'.format(error))
		print(error)
	finally:
		if conn is not None:
			conn.close()

if __name__ == "__main__":
    main(sys.argv)