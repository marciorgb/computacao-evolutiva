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


def realiza_mutacao(x_children, xfactor):
    """ Função auxiliar para realização de mutação em um único conjunto"""

    inverter = [ 1, 0]

    for j, v in enumerate(x_children):

        if r.random() < xfactor:
            x_children[j] = inverter[ x_children[j] ]

    return x_children

def mutacao(children, xfactor=0.3):
    """Realiza mutação na população fiha"""

    x_children = copy.deepcopy(children)

    for i, v in enumerate(x_children):
        x_children[i] = realiza_mutacao(x_children[i], xfactor)

    return x_children


