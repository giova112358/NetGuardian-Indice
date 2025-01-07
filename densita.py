from momento_dialogico import calcolo_momento_dialogico
from data import repertori

def calcolo_densita(analisi):
    momento_dialogico = calcolo_momento_dialogico(analisi)
    
    num = 1
    for repertorio in analisi:
        idx = repertori["repertorio"].index(repertorio)
        m = repertori["M"][idx]
        g = repertori["G"][idx]
        if (g != 0 and m != 0) :
            num *= g/m
        elif(g != 0):
            num *= g
        elif(m!= 0):
            num *= m
        else:
            num *= 1
        
        #print(f"repertorio : {repertorio} g : {g} m : {m} g/m : {g/m}" )
    
    #print(f"numeratore : {num}")
    #print(f"momento_dialogico : {momento_dialogico}")
    densita = num / momento_dialogico
    return densita, momento_dialogico
        
