import numpy as np
from itertools import chain, combinations
import math

data_dict = {
    "Repertori": ['DESCRIZIONE', 'RIFERIMENTO OBIETTIVO', 'CONSIDERAZIONE', 'PROPOSTA', 'POSSIBILITA', 'VALUTAZIONE', 'CONFERMA', 'SPECIFICAZIONE', 'PRESCRIZIONE', 'CONTRAPPOSIZIONE', 'CAUSA', 'GENERALIZZAZIONE', 'GIUDIZIO', 'COMMENTO', 'GIUSTIFICAZIONE', 'PREVISIONE', 'SANCIRE'],
    "classe": [1, 3, 5, 4, 2, 4, 3, 2, 5, 4, 3, 4, 4, 4, 4, 4, 1],
    "M": [0, 5, 11, 8, 2, 5, 2, 1, 11, 10, 3, 9, 6, 5, 8, 8, 1],
    "G": [1, 6, 12, 9, 2, 5, 1, 1, 8, 7, 1, 8, 3, 3, 5, 5, 0]
}

data_int = {
    "interazioni": ['1-1', '1-2', '1-3', '1-4', '1-5', '1-6', '2-2', '2-3', '2-4', '2-5', '2-6', '3-3', '3-4', '3-5', '3-6', '4-4', '4-5', '4-6', '5-5', '5-6', '6-6'],
    "classe 1": [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 6],
    "classe 2": [1, 2, 3, 4, 5, 6, 2, 3, 4, 5, 6, 3, 4, 5, 6, 4, 5, 6, 5, 6, 6],
    "momento classe": [10.0, 9.52380952, 9.04761904, 8.57142856, 8.09523808, 7.6190476, 7.14285712, 6.66666664, 6.19047616, 5.71428568, 5.2380952, 4.76190472, 4.28571424, 3.80952376, 3.33333328, 2.8571428, 2.38095232, 1.90476184, 1.42857136, 0.95238088, 0.4761904]
}

inter = []

def powerset(iterable):
    """Return the powerset of a given iterable."""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)) 

def calcolo_GM(data_dict, repertori_list):
    g_m = [0, 0, 0, 0, 0, 0]
    for repertorio in repertori_list:
        if repertorio in data_dict["Repertori"]:
            idx = data_dict["Repertori"].index(repertorio)
            classe = data_dict["classe"][idx]
            m = data_dict["M"][idx]
            g = data_dict["G"][idx]
            g_m[classe-1] += g+m
    return g_m
                    
def calcolo_matrix_g_m(data_dict, combs):
    matrix = []
    for comb in combs:
        matrix.append(calcolo_GM(data_dict, comb))
    return matrix

def calcolo_interazioni(g_m_matrix):
    momento_classe = data_int["momento classe"]
    momento_legame = []
    for gm in g_m_matrix:
        interazioni = []
        for i in range (1, 7):
            for j in range(i, 7):
                if(i==j):
                    interazioni.append(gm[i-1]*(gm[i-1]+1)/2)
                else:
                    interazioni.append(gm[i-1]*gm[j-1])

        with open("interazioni.txt", "a") as file:
            file.write(str(interazioni))    
        inter.append(interazioni)      
        momento_legame.append((np.array(momento_classe)*np.array(interazioni))/np.sum(np.array(interazioni)))
    return momento_legame

def calcolo_momento_dialogico(momenti_legame):
    momento_dialogico = []
    for momento in momenti_legame:
        momento_dialogico.append(sum(momento))
    return momento_dialogico

def calcolo_g_div_m(data_dict, combs):
    g_div_m_matrix = []
    for comb in combs:
        g_div_m = []
        for rep in comb:
            if rep in data_dict["Repertori"]:
                idx = data_dict["Repertori"].index(rep)
                m = float(data_dict["M"][idx])
                g = float(data_dict["G"][idx])
                if(m != 0 and g!= 0):
                    g_div_m.append(g/m)
                elif(g != 0):
                    g_div_m.append(g)
                elif(m != 0):
                    g_div_m.append(m)
        g_div_m_matrix.append(math.prod(g_div_m))
    return g_div_m_matrix
                
def calcolo_densita(g_div_matrix, momenti_dialogici):
    return np.array(g_div_matrix)/np.array(momenti_dialogici)

data_dict = {
    "Repertori": ['DESCRIZIONE', 'RIFERIMENTO OBIETTIVO', 'CONSIDERAZIONE', 'PROPOSTA', 'POSSIBILITA', 'VALUTAZIONE', 'CONFERMA', 'SPECIFICAZIONE', 'PRESCRIZIONE', 'CONTRAPPOSIZIONE', 'CAUSA', 'GENERALIZZAZIONE', 'GIUDIZIO', 'COMMENTO', 'GIUSTIFICAZIONE', 'PREVISIONE', 'SANCIRE'],
    "classe": [1, 3, 5, 4, 2, 4, 3, 2, 5, 4, 3, 4, 4, 4, 4, 4, 1],
    "M": [0, 5, 11, 8, 2, 5, 2, 1, 11, 10, 3, 9, 6, 5, 8, 8, 1],
    "G": [1, 6, 12, 9, 2, 5, 1, 1, 8, 7, 1, 8, 3, 3, 5, 5, 0]
}

data_int = {
    "interazioni": ['1-1', '1-2', '1-3', '1-4', '1-5', '1-6', '2-2', '2-3', '2-4', '2-5', '2-6', '3-3', '3-4', '3-5', '3-6', '4-4', '4-5', '4-6', '5-5', '5-6', '6-6'],
    "classe 1": [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 6],
    "classe 2": [1, 2, 3, 4, 5, 6, 2, 3, 4, 5, 6, 3, 4, 5, 6, 4, 5, 6, 5, 6, 6],
    "momento classe": [10.0, 9.52380952, 9.04761904, 8.57142856, 8.09523808, 7.6190476, 7.14285712, 6.66666664, 6.19047616, 5.71428568, 5.2380952, 4.76190472, 4.28571424, 3.80952376, 3.33333328, 2.8571428, 2.38095232, 1.90476184, 1.42857136, 0.95238088, 0.4761904]
}

repertori = data_dict['Repertori']

combination = list(powerset(repertori))

combination = combination[17:]

g_m_matrix = calcolo_matrix_g_m(data_dict, combination)

momenti_legame = calcolo_interazioni(g_m_matrix)

momenti_dialogici = calcolo_momento_dialogico(momenti_legame)

numeratore = calcolo_g_div_m(data_dict, combination)

denominatore = momenti_dialogici

densita = calcolo_densita(numeratore, momenti_dialogici)

with open("momenti_legame.txt", "w") as file:
    for comb in momenti_legame:
        file.write(str(comb)+"\n")

with open("combinazioni.txt", "w") as file:
    for comb in combination:
        file.write(str(comb)+"\n")

with open("numeratore.txt", "w") as file:
    for num in numeratore:
        file.write(str(num)+"\n")

with open("denominatore.txt", "w") as file:
    for num in denominatore:
        file.write(str(num)+"\n")
   
with open("densita.txt", "w") as file:
    for num in densita:
        file.write(str(num)+"\n")
        
densita = list(densita)
        
densita_minimo = min(densita)
densita_massimo = max(densita)

idx_min = densita.index(densita_minimo)
idx_max = densita.index(densita_massimo)

print(f" Inisieme di repertori :{combination[idx_min]} densita minimo : {densita_minimo} momento dialogico : {momenti_dialogici[idx_min]} momenti legame : {momenti_legame[idx_min]} interazioni : {inter[idx_min]} gm_matrix : {g_m_matrix[idx_min]}")
print(f" Inisieme di repertori :{combination[idx_max]} densita massimo : {densita_massimo} momento dialogico : {momenti_dialogici[idx_max]} momenti legame : {momenti_legame[idx_max]} interazioni : {inter[idx_max]} {g_m_matrix[idx_max]}")
