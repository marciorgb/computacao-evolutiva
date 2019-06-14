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


solution_size = 20 # número de soluções
conjunct_size = 36 # número de bits


def caixa_preta(
        algorithm=1,
        generations=50,
        population=[],
        is_single=False,
        is_uniform=True,
        is_elitist=True,
        is_ultra_elitist=False,
        elitism=0.85,
        xfactor=0.3,
        win_factor=1
    ):
    """Realiza o algoritmo evlutivo para o problema"""

    data_fit = []

    if algorithm == 1:
        for gen in range(generations):
            # calcula o fitness da população
            fit = fitness(population)
            # faz a seleção por torneio
            f_selec_torn, f_perd_torn = torneio(population, fit, win_factor)
            # faz o cruzamento
            child_sliced = cruzamento(f_selec_torn, is_single=is_single, is_uniform=is_uniform)
            # faz a mutação do filho
            child_mutaded = mutacao(child_sliced, xfactor=xfactor)
            # seleciona a nova população
            population = substituicao(population, father=f_selec_torn, children=child_mutaded, elitism=elitism, is_ultra_elitist=is_ultra_elitist, is_elitist=is_elitist)

            if type(population[0][0]) != int:
                import pdb;pdb.set_trace()

            fit = fitness(population)

            data_fit.append(best_fitness(fit))

    else:
        for gen in range(generations):
            # calcula o fitness da população
            fit = fitness(population)
            # calcula a média do fitness do conjunto
            fit_avg = fitness_medio(fit)
            # calcula a probabilidade de seleção
            prob_selec = selecao_prob(population, fit, fit_avg)
            # faz a seleção por rodeio
            f_selec_rol = roleta(population, prob_selec)
            # faz o cruzamento
            child_sliced = cruzamento(f_selec_rol, is_single=is_single, is_uniform=is_uniform)
            # faz a mutação do filho
            child_mutaded = mutacao(child_sliced, xfactor)
            # seleciona a nova população
            population = substituicao(population, f_selec_rol, child_mutaded, elitism, is_elitist)
            fit = fitness(population)

            data_fit.append(best_fitness(fit))

    return data_fit

def treats_data(data, typo='mean'):
    """Trata dadis para plotagem"""

    nomalized_data = []

    if typo == 'mean':
        for i, v in enumerate(data):
            nomalized_data.append( fitness_medio(data[i]) )

    if typo == 'gen_mean':
        gens = [0]*len(data[0])

        for i, v in enumerate(data):
            for j, v in enumerate(data[i]):
                gens[j] += data[i][j]
        for i,v in enumerate(gens):
            nomalized_data.append( (gens[i])/len(data[0]) )

    if typo == 'max':
        for i, v in enumerate(data):
            nomalized_data.append( max(data[i]) )

    if typo == 'gen_max':
        gens = [0]*len(data[0])

        for i, v in enumerate(data):
            for j, v in enumerate(data[i]):
                if data[i][j] > gens[j]:
                    gens[j] = (data[i][j])

        for i,v in enumerate(gens):
            nomalized_data.append( (gens[i]) )

    return nomalized_data

if __name__ == "__main__":


    data_fitness_rol = []
    data_fitness_torn = []

    data_fitness_torn_1_pc = []
    data_fitness_torn_2_pc = []
    data_fitness_torn_uniforme = []

    data_fitness_torn_high_xfactor = []
    data_fitness_torn_low_xfactor = []
    data_fitness_torn_mid_xfactor = []

    data_fitness_torn_no_elitism = []
    data_fitness_torn_high_elitism = []
    data_fitness_torn_mid_elitism = []
    data_fitness_torn_low_elitism = []
    data_fitness_torn_ultra_elitis= []


    for i in range(30):

        pop_initial = start_population(conjunct_size, solution_size)

        # standart
        data_fitness_torn.append(caixa_preta(1, 50, copy.deepcopy(pop_initial), is_elitist=False))
        data_fitness_rol.append(caixa_preta(2, 50, copy.deepcopy(pop_initial), is_elitist=False))

        # ponto de corte
        data_fitness_torn_uniforme.append(caixa_preta(1, 50, copy.deepcopy(pop_initial), is_single=False, is_uniform=True, is_elitist=False))
        data_fitness_torn_1_pc.append(caixa_preta(1, 50, copy.deepcopy(pop_initial), is_single=True, is_uniform=False, is_elitist=False))
        data_fitness_torn_2_pc.append(caixa_preta(1, 50, copy.deepcopy(pop_initial), is_single=False, is_uniform=False, is_elitist=False))

        # xFactor
        data_fitness_torn_high_xfactor.append(caixa_preta(1, 50, copy.deepcopy(pop_initial), is_single=False, is_uniform=True, is_elitist=False, xfactor=0.3))
        data_fitness_torn_mid_xfactor.append(caixa_preta(1, 50, copy.deepcopy(pop_initial), is_single=False, is_uniform=True, is_elitist=False, xfactor=0.15))
        data_fitness_torn_low_xfactor.append(caixa_preta(1, 50, copy.deepcopy(pop_initial), is_single=False, is_uniform=True, is_elitist=False, xfactor=0.075))

        # Elitismo
        data_fitness_torn_no_elitism.append(caixa_preta(1, 50, copy.deepcopy(pop_initial), is_single=False, is_uniform=True, is_elitist=False, xfactor=0.075))
        data_fitness_torn_high_elitism.append(caixa_preta(1, 50, copy.deepcopy(pop_initial), is_single=False, is_uniform=True, elitism=0.85, is_elitist=True, xfactor=0.075))
        data_fitness_torn_mid_elitism.append(caixa_preta(1, 50, copy.deepcopy(pop_initial), is_single=False, is_uniform=True, elitism=0.50, is_elitist=True, xfactor=0.075))
        data_fitness_torn_low_elitism.append(caixa_preta(1, 50, copy.deepcopy(pop_initial), is_single=False, is_uniform=True, elitism=0.30, is_elitist=True, xfactor=0.075))
        data_fitness_torn_ultra_elitis.append(caixa_preta(1, 50, copy.deepcopy(pop_initial), is_single=False, is_uniform=True, elitism=0.50, is_ultra_elitist=True ,is_elitist=True, xfactor=0.075))
        
    # TORNEIO OU ROLETA
        #   algorithm=1,
    #   generations=50,
    #   population=[],
    #   is_single=False,
    #   is_uniform=True,
    #   is_elitist=False,
    #   elitism=0.85,
    #   xfactor=0.3,
    #   win_factor=1
    # Standart


    # avg
    data_fitness_medio_torn = treats_data(data_fitness_torn, 'gen_mean')
    data_fitness_medio_rol = treats_data(data_fitness_rol, 'gen_mean')

    faz_graficos(
            data_fitness_medio_torn,
            list(range(len(data_fitness_medio_torn))),
            "Torneio & Roleta STANDART- Melhores fitness AVG",
            "Geração",
            "Fitness",
            1,
            legend="Torneio"
    )
    faz_graficos(
            data_fitness_medio_rol,
            list(range(len(data_fitness_medio_rol))),
            "Torneio & Roleta STANDART- Melhores fitness AVG",
            "Geração",
            "Fitness",
            1,
            legend="Roleta"
    )

    plt.show()
    
    # max
    data_fitness_max_rol = treats_data(data_fitness_rol, 'gen_max')
    data_fitness_max_torn = treats_data(data_fitness_torn, 'gen_max')
    
    faz_graficos(
            data_fitness_max_torn,
            list(range(len(data_fitness_max_torn))),
            "Torneio & Roleta - Melhores fitness MAX",
            "Geração",
            "Fitness",
            1,
            legend="Torneio"
    )

    faz_graficos(
            data_fitness_max_rol,
            list(range(len(data_fitness_max_torn))),
            "Torneio & Roleta - Melhores fitness MAX",
            "Geração",
            "Fitness",
            1,
            legend="Roleta"
    )

    plt.show()

    # UNIFORME, 1 PONTO DE CORTE 2 PONTOS DE CORTE
    #   algorithm=1,
    #   generations=50,
    #   population=[],
        #   is_single=False,
        #   is_uniform=True,
    #   is_elitist=False,
    #   elitism=0.85,
    #   xfactor=0.3,
    #   win_factor=1
    # Standart
    # AVG

    data_fitness_medio_torn_uniforme = treats_data(data_fitness_torn_uniforme, 'gen_mean')
    data_fitness_medio_torn_1_pc = treats_data(data_fitness_torn_1_pc, 'gen_mean')
    data_fitness_medio_torn_2_pc = treats_data(data_fitness_torn_2_pc, 'gen_mean')

    faz_graficos(
            data_fitness_medio_torn_uniforme,
            list(range(len(data_fitness_medio_torn_uniforme))),
            "Torneio Ponto de Corte- Melhores fitness AVG",
            "Geração",
            "Fitness",
            1,
            legend="Uniforme"
    )
    faz_graficos(
            data_fitness_medio_torn_1_pc,
            list(range(len(data_fitness_medio_torn_1_pc))),
            "Torneio Ponto de Corte- Melhores fitness AVG",
            "Geração",
            "Fitness",
            1,
            legend="1 Ponto de Corte"
    )
    faz_graficos(
            data_fitness_medio_torn_2_pc,
            list(range(len(data_fitness_medio_torn_2_pc))),
            "Torneio Ponto de Corte- Melhores fitness AVG",
            "Geração",
            "Fitness",
            1,
            legend="2 Pontos de Corte"
    )
    plt.show()

    # MAX

    data_fitness_max_torn_uniforme = treats_data(data_fitness_torn_uniforme, 'gen_max')
    data_fitness_max_torn_1_pc = treats_data(data_fitness_torn_1_pc, 'gen_max')
    data_fitness_max_torn_2_pc = treats_data(data_fitness_torn_2_pc, 'gen_max')

    faz_graficos(
            data_fitness_max_torn_uniforme,
            list(range(len(data_fitness_max_torn_uniforme))),
            "Torneio Ponto de Corte- Melhores fitness MAX",
            "Geração",
            "Fitness",
            1,
            legend="Uniforme"
    )
    faz_graficos(
            data_fitness_max_torn_1_pc,
            list(range(len(data_fitness_max_torn_1_pc))),
            "Torneio Ponto de Corte- Melhores fitness MAX",
            "Geração",
            "Fitness",
            1,
            legend="1 Ponto de Corte"
    )
    faz_graficos(
            data_fitness_max_torn_2_pc,
            list(range(len(data_fitness_max_torn_2_pc))),
            "Torneio Ponto de Corte- Melhores fitness MAX",
            "Geração",
            "Fitness",
            1,
            legend="2 Pontos de Corte"
    )
    plt.show()

    # Xfactor
    #   algorithm=1,
    #   generations=50,
    #   population=[],
    #   is_single=False,
    #   is_uniform=True,
    #   is_elitist=False,
    #   elitism=0.85,
        #   xfactor=0.3,
    #   win_factor=1

    #AVG

    data_fitnes_medio_torn_high_xfactor = treats_data(data_fitness_torn_high_xfactor, 'gen_mean')
    data_fitnes_medio_torn_mid_xfactor = treats_data(data_fitness_torn_mid_xfactor, 'gen_mean')
    data_fitnes_medio_torn_low_xfactor = treats_data(data_fitness_torn_low_xfactor, 'gen_mean')

    faz_graficos(
            data_fitnes_medio_torn_high_xfactor,
            list(range(len(data_fitnes_medio_torn_high_xfactor))),
            "Torneio Fator de Mutação- Melhores fitness AVG",
            "Geração",
            "Fitness",
            1,
            legend="Alto"
    )
    faz_graficos(
            data_fitnes_medio_torn_mid_xfactor,
            list(range(len(data_fitnes_medio_torn_mid_xfactor))),
            "Torneio Fator de Mutação- Melhores fitness AVG",
            "Geração",
            "Fitness",
            1,
            legend="Médio"
    )
    faz_graficos(
            data_fitnes_medio_torn_low_xfactor,
            list(range(len(data_fitnes_medio_torn_low_xfactor))),
            "Torneio Fator de Mutação- Melhores fitness AVG",
            "Geração",
            "Fitness",
            1,
            legend="Baixo"
    )
    plt.show()

    # MAX
    data_fitnes_max_torn_high_xfactor = treats_data(data_fitness_torn_high_xfactor, 'gen_max')
    data_fitnes_max_torn_mid_xfactor = treats_data(data_fitness_torn_mid_xfactor, 'gen_max')
    data_fitnes_max_torn_low_xfactor = treats_data(data_fitness_torn_low_xfactor, 'gen_max')

    faz_graficos(
            data_fitnes_max_torn_high_xfactor,
            list(range(len(data_fitnes_max_torn_high_xfactor))),
            "Torneio Fator de Mutação- Melhores fitness MAX",
            "Geração",
            "Fitness",
            1,
            legend="Alto"
    )
    faz_graficos(
            data_fitnes_max_torn_mid_xfactor,
            list(range(len(data_fitnes_max_torn_mid_xfactor))),
            "Torneio Fator de Mutação- Melhores fitness MAX",
            "Geração",
            "Fitness",
            1,
            legend="Médio"
    )
    faz_graficos(
            data_fitnes_max_torn_low_xfactor,
            list(range(len(data_fitnes_max_torn_low_xfactor))),
            "Torneio Fator de Mutação- Melhores fitness MAX",
            "Geração",
            "Fitness",
            1,
            legend="Baixo"
    )
    plt.show()

    # Elitismo

    # AVG
    data_fitnes_medio_no_elitism = treats_data(data_fitness_torn_no_elitism, 'gen_mean')
    data_fitnes_medio_high_elitism = treats_data(data_fitness_torn_high_elitism, 'gen_mean')
    data_fitnes_medio_mid_elitism = treats_data(data_fitness_torn_mid_elitism, 'gen_mean')
    data_fitnes_medio_low_elitism = treats_data(data_fitness_torn_low_elitism, 'gen_mean')
    data_fitnes_medio_ultra_elitism = treats_data(data_fitness_torn_ultra_elitis, 'gen_mean')

    faz_graficos(
            data_fitnes_medio_no_elitism,
            list(range(len(data_fitnes_medio_no_elitism))),
            "Torneio Elitismo- Melhores fitness AVG",
            "Geração",
            "Fitness",
            1,
            legend="Sem elitismo pop = pais+filhos"
    )
    faz_graficos(
            data_fitnes_medio_high_elitism,
            list(range(len(data_fitnes_medio_high_elitism))),
            "Torneio Elitismo- Melhores fitness AVG",
            "Geração",
            "Fitness",
            1,
            legend="Com elitismo Alto"
    )
    faz_graficos(
            data_fitnes_medio_mid_elitism,
            list(range(len(data_fitnes_medio_mid_elitism))),
            "Torneio Elitismo- Melhores fitness AVG",
            "Geração",
            "Fitness",
            1,
            legend="Com elitismo Médio"
    )
    faz_graficos(
            data_fitnes_medio_low_elitism,
            list(range(len(data_fitnes_medio_low_elitism))),
            "Torneio Elitismo- Melhores fitness AVG",
            "Geração",
            "Fitness",
            1,
            legend="Com elitismo Baixo"
    )
    faz_graficos(
            data_fitnes_medio_ultra_elitism,
            list(range(len(data_fitnes_medio_ultra_elitism))),
            "Torneio Elitismo- Melhores fitness AVG",
            "Geração",
            "Fitness",
            1,
            legend="Com elitismo Melhor(Pai+Filho) + Melhor(Pop)"
    )
    plt.show()

    # MAX
    data_fitnes_max_no_elitism = treats_data(data_fitness_torn_no_elitism, 'gen_max')
    data_fitnes_max_high_elitism = treats_data(data_fitness_torn_high_elitism, 'gen_max')
    data_fitnes_max_mid_elitism = treats_data(data_fitness_torn_mid_elitism, 'gen_max')
    data_fitnes_max_low_elitism = treats_data(data_fitness_torn_low_elitism, 'gen_max')
    data_fitnes_max_ultra_elitism = treats_data(data_fitness_torn_ultra_elitis, 'gen_max')

    faz_graficos(
            data_fitnes_max_no_elitism,
            list(range(len(data_fitnes_max_no_elitism))),
            "Torneio Elitismo- Melhores fitness MAX",
            "Geração",
            "Fitness",
            1,
            legend="Sem elitismo pop = pais+filhos"
    )
    faz_graficos(
            data_fitnes_max_high_elitism,
            list(range(len(data_fitnes_max_high_elitism))),
            "Torneio Elitismo- Melhores fitness MAX",
            "Geração",
            "Fitness",
            1,
            legend="Com elitismo Alto"
    )
    faz_graficos(
            data_fitnes_max_mid_elitism,
            list(range(len(data_fitnes_max_mid_elitism))),
            "Torneio Elitismo- Melhores fitness MAX",
            "Geração",
            "Fitness",
            1,
            legend="Com elitismo Médio"
    )
    faz_graficos(
            data_fitnes_max_low_elitism,
            list(range(len(data_fitnes_max_low_elitism))),
            "Torneio Elitismo- Melhores fitness MAX",
            "Geração",
            "Fitness",
            1,
            legend="Com elitismo Baixo"
    )
    faz_graficos(
            data_fitnes_max_ultra_elitism,
            list(range(len(data_fitnes_max_ultra_elitism))),
            "Torneio Elitismo- Melhores fitness MAX",
            "Geração",
            "Fitness",
            1,
            legend="Com elitismo Melhor(Pai+Filho) + Melhor(Pop)"
    )
    plt.show()
