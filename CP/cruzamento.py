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

def cruzamento(population_selected, is_single=True, is_uniform=True):
    """Realiza o cruzamento das partes envolvidas no processo"""

    children = []
    father_list = r.sample(range( len(population_selected)), len(population_selected))
    father_list.append(father_list[0])

    if is_uniform == True:
        # uniforme
        for j in range(0, len(father_list) - 1):

            children.append(
                    population_selected[ father_list[  j] ][0:int(len(population_selected[0])/2)]
                    + population_selected[ father_list[j+1] ][int(len(population_selected[0])/2): ]
            )
    else:
        if is_single == True:
            # único ponto
            slice_point = r.randint(1 ,int( len(population_selected[0])/2))

            for j in range(0, len(father_list) - 1):

                children.append(
                        population_selected[ father_list[  j] ][0:slice_point]
                        + population_selected[ father_list[j+1] ][slice_point: ]
                )

        else:
            # dois pontos
            slice_point1 = r.randint(1 ,int( len(population_selected[0])/2))
            slice_point2 = r.randint(int( len(population_selected[0])/2), int( len(population_selected[0])))

            for j in range(0, len(father_list) - 1):

                children.append(
                        population_selected[ father_list[  j] ][0:slice_point1]
                        + population_selected[ father_list[j+1] ][slice_point1: slice_point2]
                        + population_selected[ father_list[j] ][slice_point2: ]
                )

    return children
