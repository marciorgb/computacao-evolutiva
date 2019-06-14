from statistics import mean
from codificacao import start_population 
from fitness import *
from Seleção import *
from cruzamento import *
from substituição import *
from graficos import *

import matplotlib.pyplot as plt
import random as r
import copy
import time

def selecao_prob(population, fitness, fitness_avg):
    """Faz o cálclulo do fitness proporcional"""

    prob_selection = []

    for i, val in enumerate(population):
        prob_selection.append( fitness[i]/(len(population) * fitness_avg) )

    return prob_selection

def roleta(population, prob_selection):
    """Algoritmo de seleção baseado em roleta"""

    roullette = []
    weight = []

    for i, val in enumerate(prob_selection):
        if prob_selection[i] < 0.10:

            weight.append(1)
        elif prob_selection[i] < 0.11:

            weight.append(2)
        elif prob_selection[i] < 0.20:

            weight.append(4)
        elif prob_selection[i] < 0.40:

            weight.append(6)
        elif prob_selection[i] < 0.60:

            weight.append(8)
        elif prob_selection[i] < 1:

            weight.append(10)

    tmp = sum(weight)

    for j in range( int( len(population)/2 ) ):

        rand = r.randint(0, tmp)
        sum_roullette = 0
        i = 0

        while sum_roullette < rand:

            sum_roullette += weight[i]
            i += 1

        roullette.append( population[i-1] )

    return roullette

def torneio(population, fitness, win_factor=1):
    """Algoritmo de seleção baseado no modelo de torneio"""

    tournment = []
    loser = []
    chain = r.sample(range( len(population) ), len(population))

    for j in range(0 ,int( len(population) ), 2):

        if fitness[ chain[j] ] < fitness[ chain[j+1] ]:
            maior = fitness[ chain[j+1] ]
            menor = fitness[ chain[j] ]

        else:
            maior = fitness[ chain[j] ]
            menor = fitness[ chain[j+1] ]

        if r.random() < win_factor:
            tournment.append(population[ fitness.index( maior ) ])
            loser.append(population[ fitness.index( menor ) ])

        else:
            tournment.append(population[ fitness.index( menor ) ])
            loser.append(population[ fitness.index( menor ) ])

    return tournment, loser
