from statistics import mean
import matplotlib.pyplot as plt
import random as r
import sys
import copy
import time
import math

restrict = False
solution_size = 30 # número de soluções
dimension = 10  # número de dimenções N
negative_limit = -5.12
positive_limit = 5.12
gen = 0
aval_fo = 0
best_of_all = []
best_indv_all = []

###############################################################################
def start_conjunct (dimension, negative_limit, positive_limit):
    """inicializa solução"""

    conjunct = []

    for i in range(dimension):
        conjunct.append( r.uniform(negative_limit, positive_limit))

    return conjunct

def conjunct_is_invalid (population, last):
    """verifica validade do conjunto"""

    for i, val in enumerate(population):

        if population[i] == population[last] and i != last:
            return True
    return False

def start_population (dimension, negative_limit, positive_limit, solution_size):
    """inicializa população de soluções"""

    population = []

    for i in range(solution_size):
        population.append( start_conjunct(dimension, negative_limit, positive_limit) )

        while conjunct_is_invalid(population, i): #verifica se o conjunto já existe

            population.pop()
            population.append( start_conjunct(conjunct_size) )

    return population

###############################################################################
def solution(conjunct, n, A=10, is_restrict=False):
    """Calculo do Fintess"""
    global aval_fo
    aval_fo += 1
    sum_r = []
    sol = 0
    for i, v in enumerate(conjunct):
        sol = conjunct[i]**2 - 10*math.cos(2*math.pi*conjunct[i])
        if check_limits(conjunct[i]) and is_restrict:
            sol += 10000
            print(sol)
        sum_r.append(sol)

    return A*n + math.fsum(sum_r)

def fitness(population, n, A=10, is_restrict=False):
    """Calculo do fitness e atribuição em vetor de fitness"""
    global restrict

    fitness = []

    for i, val in enumerate(population):
        fitness.append( solution(population[i], n, A, is_restrict=restrict) )

    return fitness

def order_by_fitness(population=[], fitness=[], is_reverse=False):
    """Ordena pelo Fitness"""

    zipped_population = zip(population, fitness)
    sorted_zipped = sorted(zipped_population, key=lambda i: i[1], reverse = is_reverse)
    
    return [sorted_pop[0] for sorted_pop in sorted_zipped]

def fitness_medio(fitness):
    """Faz o cálculo do valor médio de fitness do conjunto"""

    return mean(fitness)

def best_fitness(fitness):
    """Pega o melhor fitness da população"""

    return min(fitness)

###############################################################################
def torneio(population, fitness, win_factor=1):
    """Algoritmo de seleção baseado no modelo de torneio"""

    tournment = []
    loser = []
    chain = r.sample(range( len(population) ), len(population))

    for j in range(0 ,int( len(population) ), 2):

        if fitness[ chain[j] ] > fitness[ chain[j+1] ]:
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

    return tournment

###############################################################################
def cruzamento(population_selected, is_single=True, is_uniform=True, is_recombination=False):
    """Realiza o cruzamento das partes envolvidas no processo"""

    children = []
    father_list = r.sample(range( len(population_selected)), len(population_selected))
    father_list.append(father_list[0])

    if is_recombination == True:
        for j in range(0, len(father_list) - 1):
            recomb = []
            for i, v in enumerate(population_selected[father_list[j]]):
                recomb.append(
                    population_selected[father_list[j]][i]
                    + (population_selected[father_list[j+1]][i] - population_selected[father_list[j]][i])*r.random()
                )
            children.append(recomb)

    elif is_uniform == True:
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
                        population_selected[ father_list[  j] ][:slice_point]
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

###############################################################################
def check_limits(x):
    """Verifica limites de restrição"""
    g = math.sin(2*math.pi*x) + 0.5
    h = math.cos(2*math.pi*x) + 0.5

    if h < 0.0001:
        h = 0

    if g > 0 or h != 0:
        return True
    return False

def realiza_mutacao(x_children, xfactor, is_restrict):
    """ Função auxiliar para realização de mutação em um único conjunto"""
    global positive_limit, negative_limit

    for j, v in enumerate(x_children):

        if r.random() < xfactor:
            new_value = x_children[j] + x_children[j]*r.uniform(-0.85, 0.85)
            if new_value < positive_limit and new_value > negative_limit:
                x_children[j] = new_value

    return x_children

def mutacao(children, xfactor=0.3, is_restrict=False):
    """Realiza mutação na população fiha"""

    x_children = copy.deepcopy(children)

    for i, v in enumerate(x_children):
        x_children[i] = realiza_mutacao(x_children[i], xfactor, is_restrict)

    return x_children

###############################################################################
def substituicao(
        population,
        father,
        children,
        elitism=0.85,
        is_elitist=True,
        is_ultra_elitist=False,
        loser=[],
        is_loser=False,
        dimension=3,
        is_restrict=False):
    """Realiza substituição do conjunto de dados"""
    
    father_order = order_by_fitness(father, fitness(father, dimension, is_restrict=is_restrict), False)

    children_order = order_by_fitness(children, fitness(children, dimension, is_restrict=is_restrict), False)

    population = order_by_fitness(population, fitness(population, dimension, is_restrict=is_restrict), True)

    if is_ultra_elitist == True:
        best_pop = father_order + children_order
        best_gen = order_by_fitness(best_pop, fitness(best_pop, dimension, is_restrict=is_restrict), False)
        population = order_by_fitness(population, fitness(population, dimension, is_restrict=is_restrict), True)
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

###############################################################################
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
                x_data[i].sort(reverse=True)
        else:
            x_data.sort(reverse=True)

    if in_depth == 2:
        for i, v in enumerate(x_data):

            plt.plot(y_data, x_data[i])
    else:
        plt.plot(y_data, x_data, label=legend)
    plt.legend().get_frame().set_facecolor('C0')

def trata_dados(data, typo='mean'):
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

    if typo == 'min':
        for i, v in enumerate(data):
            nomalized_data.append( min(data[i]) )

    if typo == 'gen_min':
        gens = [sys.maxsize]*len(data[0])

        for i, v in enumerate(data):
            for j, v in enumerate(data[i]):
                if data[i][j] < gens[j]:
                    gens[j] = (data[i][j])
        for i,v in enumerate(gens):
            nomalized_data.append( (gens[i]) )

    return nomalized_data

###############################################################################
def comp_evo(
        generations=50,
        population=[],
        is_single=False,
        is_uniform=True,
        is_elitist=True,
        is_ultra_elitist=False,
        elitism=0.85,
        xfactor=0.3,
        win_factor=1,
        dimension=3,
        is_recombination=False,
        is_ofaval=False,
        is_restrict=False,
    ):
    """Realiza o algoritmo evlutivo para o problema"""

    global aval_fo, gen, best_of_all, best_idnv_all
    data_fit = [] 
    if is_ofaval == True:
        #while aval_fo < 10000 and gen < 50:
        while gen < 50:
            # calcula o fitness da população
            fit = fitness(population, dimension, is_restrict=is_restrict)
            # faz a seleção por torneio
            f_selec_torn = torneio(population, fit, win_factor)
            # faz o cruzamento
            child_sliced = cruzamento(f_selec_torn, is_single=is_single, is_uniform=is_uniform, is_recombination=is_recombination)
            # faz a mutação do filho
            child_mutaded = mutacao(child_sliced, xfactor=xfactor, is_restrict=is_restrict)
            # seleciona a nova população
            population = substituicao(population, father=f_selec_torn, children=child_mutaded, elitism=elitism, is_ultra_elitist=is_ultra_elitist, is_elitist=is_elitist)
            fit = fitness(population, dimension, is_restrict=is_restrict)
            gen += 1
            best_of_all.append( [best_fitness(fit), gen, population[0]])
            if best_fitness(fit) < 0.04:
                best_indv_all.append([ gen, best_fitness(fit),population])
            data_fit.append(best_fitness(fit))
    else:
        time_cpu_start = time.time()
        time_cpu = time_cpu_start - time.time()
        while time_cpu < 180.0 or gen == 0:
            # calcula o fitness da população
            fit = fitness(population, dimension)
            # faz a seleção por torneio
            f_selec_torn = torneio(population, fit, win_factor)
            # faz o cruzamento
            child_sliced = cruzamento(f_selec_torn, is_single=is_single, is_uniform=is_uniform, is_recombination=is_recombination)
            # faz a mutação do filho
            child_mutaded = mutacao(child_sliced, xfactor=xfactor)
            # seleciona a nova população
            population = substituicao(population, father=f_selec_torn, children=child_mutaded, elitism=elitism, is_ultra_elitist=is_ultra_elitist, is_elitist=is_elitist)
            fit = fitness(population, dimension)
            gen += 1
            data_fit.append(best_fitness(fit))
            time_cpu = time.time() - time_cpu_start

    return data_fit

###############################################################################
if __name__ == "__main__":


    dados_fitness = []
    dados_fitness_restrict = []
    sr = []
    sr1 = []

    for i in range(100):
        pop_initial = start_population(dimension, negative_limit, positive_limit, solution_size)
        gen = 0
        # Elitismo
        restrict = False
        dados_fitness.append(
                comp_evo(
                    50,
                    copy.deepcopy(pop_initial),
                    is_single=False,
                    is_uniform=True,
                    elitism=0.50,
                    is_ultra_elitist=True,
                    is_elitist=True,
                    xfactor=0.075,
                    dimension=dimension,
                    is_recombination=True,
                    is_ofaval=True,
                    is_restrict=False
                )
        )
        gen = 0
        restrict = True
        sr.append(min(copy.deepcopy(best_of_all)))
        best_of_all = []
        dados_fitness_restrict.append(
                comp_evo(
                    50,
                    copy.deepcopy(pop_initial),
                    is_single=False,
                    is_uniform=True,
                    elitism=0.50,
                    is_ultra_elitist=True,
                    is_elitist=True,
                    xfactor=0.075,
                    dimension=dimension,
                    is_recombination=True,
                    is_ofaval=True,
                    is_restrict=True
                )
        )
        gen = 0
        sr1.append(min(copy.deepcopy(best_of_all)))
        best_of_all = []

###############################################################################
    dados_fitnes_medio = trata_dados(dados_fitness, 'gen_mean')
    dados_fitnes = trata_dados(dados_fitness, 'gen_min')

    faz_graficos(

            dados_fitnes,
            list(range(len(dados_fitnes))),
            "Irrestrito",
            "Fitness",
            "Geração",
            legend="Mínimo",
            is_sorted=False,
            in_depth=1
    )
    faz_graficos(
            dados_fitnes_medio,
            list(range(len(dados_fitnes_medio))),
            "Irrestrito",
            "Fitness",
            "Geração",
            legend="Médio",
            is_sorted=True,
            in_depth=1
    )
    plt.show()
    print(min(sr))
###############################################################################
    dados_fitnes_medio_restrict = trata_dados(dados_fitness_restrict, 'gen_mean')
    dados_fitnes_restrict = trata_dados(dados_fitness_restrict, 'gen_min')
     
    faz_graficos(
             dados_fitnes_restrict,
            list(range(len(dados_fitnes_restrict))),
            "Restrito",
            "Fitness",
            "Geração",
            legend="Mínimo",
            is_sorted=False,
            in_depth=1
    )
    faz_graficos(
            dados_fitnes_medio_restrict,
            list(range(len(dados_fitnes_medio_restrict))),
            "Restrito",
            "Fitness",
            "Geração",
            legend="Médio",
            is_sorted=True,
            in_depth=1
    )
    plt.show()
    print(min(sr1))
    #
