from numero_interazioni import calcolo_numero_interazioni
from frequenza import calcolo_frequenza
from data import interazioni
import numpy as np

def calcolo_momento_legame(analisi):
    frequenza = calcolo_frequenza(analisi)
    numero_interazioni = calcolo_numero_interazioni(frequenza)
    interazioni['numero_interazioni'] = numero_interazioni
    
    
    numero_interazioni = np.array(interazioni['numero_interazioni'])
    momento_classe = np.array(interazioni['momento_classe'])
    momento_legame = (numero_interazioni*momento_classe)/numero_interazioni.sum()
    
    return momento_legame

