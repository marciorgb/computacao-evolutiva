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


def solution(conjunct):
    """Valor da solução, feito para calcular o fintess"""

    off_signal = (
        9
        + conjunct[ 1] * conjunct[ 4] - conjunct[22] * conjunct[13]
        + conjunct[23] * conjunct[ 3] - conjunct[20] * conjunct[ 9]
        + conjunct[35] * conjunct[14] - conjunct[10] * conjunct[25]
        + conjunct[15] * conjunct[16] + conjunct[ 2] * conjunct[32]
        + conjunct[27] * conjunct[18] + conjunct[11] * conjunct[33]
        - conjunct[30] * conjunct[31] - conjunct[21] * conjunct[24]
        + conjunct[34] * conjunct[26] - conjunct[28] * conjunct[ 6]
        + conjunct[ 7] * conjunct[12] - conjunct[ 5] * conjunct[ 8]
        + conjunct[17] * conjunct[19] - conjunct[ 0] * conjunct[29]
        + conjunct[22] * conjunct[ 3] + conjunct[20] * conjunct[14]
        + conjunct[25] * conjunct[15] + conjunct[30] * conjunct[11]
        + conjunct[24] * conjunct[18] + conjunct[ 6] * conjunct[ 7]
        + conjunct[ 8] * conjunct[17] + conjunct[ 0] * conjunct[32]
        )

    return off_signal

def fitness(population):
    """Calculo do fitness e atribuição em vetor de fitness"""

    fitness = []

    for i, val in enumerate(population):
        fitness.append( solution(population[i]) )

    return fitness

def fitness_medio(fitness):
    """Faz o cálculo do valor médio de fitness do conjunto"""

    return mean(fitness)

def best_fitness(fitness):
    """Pega o melhor fitness da população"""

    return max(fitness)

def order_by_fitness(population=[], fitness=[], is_reverse=True):
    """Ordena pelo melhor Fitness"""

    zipped_population = zip(population, fitness)

    sorted_zipped = sorted(zipped_population, key=lambda i: i[1], reverse = is_reverse)
    
    return [sorted_pop[0] for sorted_pop in sorted_zipped]
