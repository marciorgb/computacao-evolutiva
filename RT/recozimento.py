from statistics import mean
import matplotlib.pyplot as plt
import random as r
import copy
import time
import math

aval_fo = 0
is_restrict = False 

def check_limits(x):
    """Verifica limites de restrição"""
    g = math.sin(2*math.pi*x) + 0.5
    h = math.cos(2*math.pi*x) + 0.5

    if h < 0.0001:
        h = 0

    if g > 0 or h != 0:
        return True
    return False

def solucao(conjunct, n, A=10):
    """Calculo do Fintess"""
    global aval_fo, is_restrict
    aval_fo += 1
    sum_r = []
    sol = 0
    for i, v in enumerate(conjunct):
        sol = conjunct[i]**2 - 10*math.cos(2*math.pi*conjunct[i])
        if check_limits(conjunct[i]) and is_restrict:
            sol += 100
        sum_r.append(sol)

    return A*n + math.fsum(sum_r)

def vizinhanca(indv, forca):
    """Next(indv)"""

    indv_old = indv[:]

    while indv == indv_old:
        for j, v in enumerate(indv):
            if r.random() < 0.3:
                indv[j] = indv[j] + r.uniform(-forca, forca)*indv[j]

    return indv 
###############################################################################
def prob_mudaca(ei, ej , kb, t):
    """B = Boltzmann e T temperatura"""

    return math.exp(-(ej-ei)/(kb*t))

def prob_aceite(indv, indv_j, c, n):
    """Probabilidade de Aceite de um indivíduo J"""
    if solucao(indv_j, n) > solucao(indv_f, n):
        pc = 1
    else:
        pc = math.exp((solucao(indv, n) - solucao(indv_j, n))/c)

    return pc

###############################################################################
def recozimento(indv, n, alpha, forca,t0, tf, sf, inter_max):
    """ indv = sol inicial
        t0    = temperatura inicial
        tf    = temperatura final
        sf    = valor desejado
    """
    global aval_fo

    t = t0
    best = [solucao(indv, n), indv]

    while (t > tf and solucao(indv, n) > sf):

        for i in range(inter_max):

            indv_d = vizinhanca(indv, forca)
            delta = solucao(indv_d, n) - solucao(indv, n)

            if delta < 0:
                indv = indv_d

                if solucao(indv, n) < solucao(best[1], n):
                     best = [solucao(indv, n), indv]

            elif r.random() < math.exp(- delta/t):
                indv = indv_d

        t = t*alpha
    best = [solucao(indv, n), indv]

    return best

###############################################################################
def individuo_inicial(dimensao, lm_negativo, lm_positivo):
    """inicializa solução"""

    conjunct = []

    for i in range(dimensao):
        conjunct.append( r.uniform(lm_negativo, lm_positivo))

    return conjunct

###############################################################################
def faz_graficos(
        x_data,
        y_data,
        title='grafico',
        x_title='dados',
        y_title='execuções',
        in_depth=1,
        legended=True,
        legend='dado'
    ):
    """Realiza a plotagem dos gráficos dos resultados"""

    plt.title(title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.grid(True)

    plt.plot(y_data, x_data, label=legend)
    plt.legend().get_frame().set_facecolor('C0')

def trata_dados(data):
    """Trata dadis para plotagem"""

    nomalized_data = []

    for i, v in enumerate(data):
        nomalized_data.append(data[i][0])

    return nomalized_data
###############################################################################
if __name__ == "__main__":

    dimensao = 3
    t0 = 1e3
    tf = 1e-6
    alpha = 0.8
    inter_max = dimensao*10
    forca = 0.5
    lm_negativo = -5.12
    lm_positivo = 5.12

    resposta = []
    for i in range(100):
        resposta.append( 
                recozimento(
                    indv=individuo_inicial(dimensao, lm_negativo, lm_positivo),
                    n=dimensao,
                    alpha=alpha,
                    forca=forca,
                    t0=t0,
                    tf=tf,
                    sf=1e-6,
                    inter_max=inter_max
                )
        )
    
    data_resposta = trata_dados(resposta)
    m_resp = min(resposta)
    print("O melhor valor foi: {}".format(min(data_resposta)))
    print("O melhor indivíduo foi: {}".format(m_resp[1]))
        
    faz_graficos(
            data_resposta,
            list(range(len(data_resposta))),
            "RECOZIMENTO SIMULADO \n Fitness {}\n Indvíduo: {}".format(m_resp[0],m_resp[1]),
            "Teste",
            "Fitness",
            1,
            legend="Recozimento Simulado"
    )
    plt.show()
