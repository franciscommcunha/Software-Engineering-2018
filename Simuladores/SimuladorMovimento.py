# -*- coding: utf-8 -*-
import sys
import time
from random import randint

################# CONSTANTES #################

## intervalo de atualização (segundos)
INTERVALO_DE_TEMPO = 1
LUMINOSIDADE_INICIAL = 0
PERC_TEMPO_HA_MOVIM = 5

DIVISOES = ['cozinha', 'sala', 'quarto1', 'quarto2']
##############################################

def main(argv):
    divisoes = DIVISOES
    luminosidade = [LUMINOSIDADE_INICIAL, LUMINOSIDADE_INICIAL, LUMINOSIDADE_INICIAL, LUMINOSIDADE_INICIAL]
    while True:
        movimento = []
        for divisao in divisoes:
            movimento.append([divisao, False])

        movimento = calcMovimento(movimento)
        luminosidade = checkMovimento(movimento, luminosidade)
        imprimir(movimento, luminosidade)

        time.sleep(INTERVALO_DE_TEMPO)

def calcMovimento(movimento):
    i = 0
    for a,b in movimento:
        rand = (randint(0, 100))
        if rand < PERC_TEMPO_HA_MOVIM:
            b = True
            movimento[i] = [a,b]
        i += 1

    return movimento

def checkMovimento(movimento, luminosidade):
    i=0
    for a,b in movimento:
        if b==True:
            luminosidade[i]=1
        else:
            luminosidade[i]=0    
        i+=1
    return luminosidade        
    


def imprimir(movimento, luminosidade):
    #print(movimento)
    listaDeMovimento = []
    i = 0
    for a,b in movimento:
        if b == True:
            listaDeMovimento.append([a, luminosidade[i]])  
        i += 1
    if len(listaDeMovimento) > 0:
        print(listaDeMovimento)
    print("---------\n")

if __name__ == "__main__":
    main(sys.argv)