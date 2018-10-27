import sys
import time
import send
import send_kafka
from random import randint

################# UNIDADES #################
# temperatura       ºC
# CO2               ppm
# humidade          %
############################################

################# CONSTANTES #################

## intervalo de atualização (minutos)
INTERVALO_DE_TEMPO = 1

TEMPERATURA_MIN = 10
TEMPERATURA_MAX = 25
TEMPERATURA_INICIAL = 16

CO2_MIN = 300
CO2_MAX = 900
CO2_INICIAL = 600

HUMIDADE_MIN = 10
HUMIDADE_MAX = 90
HUMIDADE_INICIAL = 55

PERC_TEMPO_HA_MOVIM = 5

DIVISOES = ['cozinha', 'sala', 'quarto1', 'quarto2']
##############################################

def main(argv):
    temperatura = TEMPERATURA_INICIAL
    co2 = CO2_INICIAL
    humidade = HUMIDADE_INICIAL

    while True:
        temperatura = calcTemperatura(temperatura)
        co2 = calcCO2(co2)
        humidade = calcHumidade(humidade)

        ##ADDED
        send.send(str(temperatura))
        #send_kafka.send(str(temperatura))
        send.send(str(co2))
        #send_kafka.send(str(co2))
        send.send(str(humidade))
        #send_kafka.send(str(humidade))
        #imprimir(temperatura, co2, humidade)
        time.sleep(INTERVALO_DE_TEMPO * 60)

def calcTemperatura(x):
    rand = (randint(-2, 2))
    if x + rand < TEMPERATURA_MIN:
        return TEMPERATURA_MIN
    elif x + rand > TEMPERATURA_MAX:
        return TEMPERATURA_MAX
    else:
        return x + rand

def calcCO2(x):
    rand = (randint(-50, 50))
    if x + rand < CO2_MIN:
        return CO2_MIN
    elif x + rand > CO2_MAX:
        return CO2_MAX
    else:
        return x + rand

def calcHumidade(x):
    rand = (randint(-5, 5))
    if x + rand < HUMIDADE_MIN:
        return HUMIDADE_MIN
    elif x + rand > HUMIDADE_MAX:
        return HUMIDADE_MAX
    else:
        return x + rand

def imprimir(temperatura, co2, humidade):
    print("Temperatura\n", temperatura)
    print("CO2\n", co2)
    print("Humidade\n", humidade)
    print("---------\n")

if __name__ == "__main__":
    main(sys.argv)