from densita import calcolo_densita
from data import repertori
from itertools import chain, combinations
import pandas as pd
import json

def powerset(iterable):
    """Return the powerset of a given iterable."""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)) 

reps = repertori['repertorio']

combs = list(powerset(reps))

combs = combs[17:]

print(f"Numero di combinazioni : {len(combs)}")

if __name__=="__main__":
    analisi = []
    md = []
    dens = []
    
    for comb in combs:
        densita, momento_dialogico = calcolo_densita(list(comb))
        analisi.append(comb)  
        md.append(momento_dialogico)
        dens.append(densita)
            
    sheet = {
        'analisi' : analisi,
        'momento_dialogico' : md,
        'densita' : dens
    }
    
    print(sheet['momento_dialogico'])
    
    # Convert dictionary to DataFrame
    df = pd.DataFrame(sheet)

    # Save DataFrame to Excel file
    df.to_excel("output.xlsx", index=False)
    