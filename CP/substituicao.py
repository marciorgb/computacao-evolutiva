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


def substituicao(population, father, children, elitism=0.85, is_elitist=True, is_ultra_elitist=False, loser=[], is_loser=False):
    """Realiza substituição do conjunto de dados"""
    
    father_order = order_by_fitness(father, fitness(father), True)

    children_order = order_by_fitness(children, fitness(children), True)

    population = order_by_fitness(population, fitness(population), False)

    if is_ultra_elitist == True:
        best_pop = father_order + children_order
        best_gen = order_by_fitness(best_pop, fitness(best_pop), True)
        population = order_by_fitness(population, fitness(population), False)
        slice_point = int(len(population)*elitism)
        population = best_gen[0:slice_point] + population[slice_point:]

    elif is_elitist:

        for i in range(int(len(population)/2)):

            if r.random() < elitism:
                if children_order[i] > father_order[i]:
                    population[i] = children_order[i]
                else:
                    population[i] = father_order[i]
            else:
                population[i] = children_order[i]
        
        if is_loser:
            for i in range(int(len(population)/2)):
                population[int(len(population)/2) + i] = loser[i]

    else:

        population = father_order + children_order

    return population
