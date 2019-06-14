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


def start_conjunct (conjunct_size):
    """inicializa solução"""

    conjunct = []

    for i in range(conjunct_size):
        conjunct.append( r.randint(0, 1))

    return conjunct

def conjunct_is_invalid (population, last):
    """verifica validade do conjunto"""

    for i, val in enumerate(population):

        if population[i] == population[last] and i != last:
            return True
    return False

def start_population (conjunct_size, solution_size):
    """inicializa população de soluções"""

    population = []

    for i in range(solution_size):
        population.append( start_conjunct(conjunct_size) )

        while conjunct_is_invalid(population, i): #verifica se o conjunto já existe

            population.pop()
            population.append( start_conjunct(conjunct_size) )

    return population

