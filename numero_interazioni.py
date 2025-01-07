from data import interazioni
    
def calcolo_numero_interazioni(frequenza):
    numero_interazioni = []
    gm = frequenza['calcolo_g_m']
    for i in range (1, 7):
        for j in range(i, 7):
            if(i==j):
                numero_interazioni.append(gm[i-1]*(gm[i-1]+1)/2)
            else:
                numero_interazioni.append(gm[i-1]*gm[j-1])
    
    return numero_interazioni
    
