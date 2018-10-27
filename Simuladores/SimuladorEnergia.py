# -*- coding: utf-8 -*-
import sys
import time
from random import randint

################# CONSTANTES #################

## intervalo de atualização (segundos)
INTERVALO_DE_TEMPO = 3600

#['aparelho', gastoPorHoraWatts, %tempoLigado]
APARELHOS = [ ['tv', 120, 0.4], ['luz_quarto', 60,  0.2], ['aquecedor', 2000, 0.15], ['frigorifico', 100, 1] ]
##############################################

def main(argv):
    aparelhos = APARELHOS

    while True:
        gastoNaUltimaHora = []
        for aparelho in aparelhos:
            gastoNaUltimaHora.append([aparelho[0], 0])

        gastoNaUltimaHora = calcEnergia(gastoNaUltimaHora, aparelhos)

        imprimir(gastoNaUltimaHora)
        
        for x in gastoNaUltimaHora:
           appliance = x[0]
           value = x[1]

        time.sleep(INTERVALO_DE_TEMPO)

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

def imprimir(gastoNaUltimaHora):
    print(gastoNaUltimaHora)

if __name__ == "__main__":
    main(sys.argv)