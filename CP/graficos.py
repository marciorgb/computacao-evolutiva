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


def faz_graficos(
        x_data,
        y_data,
        title='grafico',
        x_title='dados',
        y_title='execuções',
        in_depth=2,
        legended=True,
        is_sorted=True,
        legend='dado'
    ):
    """Realiza a plotagem dos gráficos dos resultados"""

    plt.title(title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.grid(True)

    if is_sorted == True:
        if in_depth == 2:
            for i, v in enumerate(x_data):
                x_data[i].sort()
        else:
            x_data.sort()

    if in_depth == 2:
        for i, v in enumerate(x_data):

            plt.plot(y_data, x_data[i])
    else:
        plt.plot(y_data, x_data, label=legend)
    plt.legend().get_frame().set_facecolor('C0')

