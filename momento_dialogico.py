from momento_legame import calcolo_momento_legame

def calcolo_momento_dialogico(analisi):
    momento_legame = calcolo_momento_legame(analisi)
    momento_dialogico = momento_legame.sum()
    
    return momento_dialogico
    
