# -*- coding: utf-8 -*-

import sys
import time
from random import randint

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

LUMINOSIDADE_MIN=0
LUMINOSIDADE_MAX=1
LUMINOSIDADE_INICIAL=0

PERC_TEMPO_HA_MOVIM = 5

DIVISOES = ['cozinha', 'sala', 'quarto1', 'quarto2']
##############################################

def main(argv):
    divisoes = DIVISOES
    #temperatura = [TEMPERATURA_INICIAL, TEMPERATURA_INICIAL, TEMPERATURA_INICIAL, TEMPERATURA_INICIAL]
    #co2 = [CO2_INICIAL, CO2_INICIAL, CO2_INICIAL, CO2_INICIAL]
    #humidade = [HUMIDADE_INICIAL, HUMIDADE_INICIAL, HUMIDADE_INICIAL, HUMIDADE_INICIAL]
    #luminosidade = [LUMINOSIDADE_INICIAL, LUMINOSIDADE_INICIAL, LUMINOSIDADE_INICIAL, LUMINOSIDADE_INICIAL]

    atuadorTemperatura = []
    temperatura = []
    co2 = []
    humidade = []
    luminosidade = []

    for x in range(0, len(DIVISOES)):
        atuadorTemperatura.append( False )
        temperatura.append( TEMPERATURA_INICIAL )
        co2.append( CO2_INICIAL )
        humidade.append( HUMIDADE_INICIAL )
        luminosidade.append( LUMINOSIDADE_INICIAL )

    while True:
        temperatura = calcTemperatura( temperatura, atuadorTemperatura )
        co2 = calcCO2(co2)
        humidade = calcHumidade(humidade)
        luminosidade=calcLuminosity(luminosidade)

        imprimir(divisoes, temperatura, co2, humidade, luminosidade)
        time.sleep(INTERVALO_DE_TEMPO * 15)

def calcTemperatura( lista, atuadorTemperatura ):
    i = 0
    for x in lista:
        if atuadorTemperatura[i] == True:
            print( "TRUE" )
        else:
            rand = (randint(-2, 2))
            if x + rand < TEMPERATURA_MIN:
                lista[i] = TEMPERATURA_MIN
            elif x + rand > TEMPERATURA_MAX:
                lista[i] = TEMPERATURA_MAX
            else:
                lista[i] = x + rand
        i += 1
    return lista

def calcCO2( lista ):
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
    return lista

def calcLuminosity(lista):
	i=0
	for x in lista:
		rand = (randint(0,1))
		lista[i]=rand
		i+=1
	return lista			


def calcHumidade( lista ):
    i = 0
    for x in lista:
        rand = (randint(-5, 5))
        if x + rand < HUMIDADE_MIN:
            lista[i] = HUMIDADE_MIN
        elif x + rand > HUMIDADE_MAX:
            lista[i] = HUMIDADE_MAX
        else:
            lista[i] = x + rand
        i += 1
    return lista

def imprimir(divisoes, temperatura, co2, humidade, luminosidade):
    i = 0
    lista = []
    for x in divisoes:
        lista.append( [x, "temp:", temperatura[i], "co2:", co2[i], "hum:", humidade[i], "lum:", luminosidade[i]] )
        i += 1

    print(lista)

    #print("Temperatura\n", temperatura)
    #print("CO2\n", co2)
    #print("Humidade\n", humidade)
    #print("---------\n")

if __name__ == "__main__":
    main(sys.argv)