from data import repertori, classi

def calcolo_frequenza(analisi):
    calcolo_g_m = [0, 0, 0, 0, 0, 0]
    frequenza_classi = [0, 0, 0, 0, 0, 0]
    for repertorio in analisi:
        if repertorio in repertori["repertorio"]:
            idx = repertori["repertorio"].index(repertorio)
            classe = repertori["classe"][idx]
            m = repertori["M"][idx]
            g = repertori["G"][idx]
            calcolo_g_m[classe-1] += g+m
            frequenza_classi[classe-1] += 1
    
    frequenza = {
        'classe' : classi,
        'frequenza' : frequenza_classi,
        'calcolo_g_m' : calcolo_g_m
    }
    
    return frequenza
    

if __name__=="__main__":
    frequenza = calcolo_frequenza(['CONSIDERAZIONE', 'PROPOSTA'])
    print(frequenza)
