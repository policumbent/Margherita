#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 18:06:19 2022

@author: felixackermann
"""

import csv
import numpy as np
import matplotlib.pylab as plt 
import matplotlib.pyplot as plt_pyplot
import pywt as pwt
import statistics as st
from scipy import fftpack as f 

i=0
M = np.zeros((2061,5))
with open('2021_10_24__12_29_17.csv',newline='') as csvfile:
    for row in csvfile.readlines()[1:]: #salto prima riga
        dummy = row.strip().split(',')
        for j in range(5):
                M[i][j] = float(dummy[j+1])
        i+=1 

n=int(np.size(M, axis=0))  
v = np.float_([M[i][3] for i in range(n)]) # non posso usare : per array multidimensionale
durata_int = 900 # lunghezza dell'intervallo in s
t = np.zeros((int(np.round(n/durata_int)),5)) # per caratterizzare intervalli di 15min

# filtro di media
param_3 = 3
h = 1/param_3*np.ones(param_3)
V = np.convolve(v,h,'valid')
n_rid= int(np.size(V,axis=0))

i=1
bool = True
while bool:
    t[i-1][0] = np.percentile(V[durata_int*(i-1):durata_int*i],25)
    t[i-1][1] = np.percentile(V[durata_int*(i-1):durata_int*i],50)
    t[i-1][2] = np.percentile(V[durata_int*(i-1):durata_int*i],75)
    t[i-1][3] = np.mean(V[durata_int*(i-1):durata_int*i])
    t[i-1][4] = np.sqrt(np.mean(np.power(V[durata_int*(i-1):durata_int*i],2)))
    
    if n-durata_int*i >= durata_int:
        i += 1
    else:
        bool = False
        
        
# Def. variabili per conteggio raffiche per tutto il file
"""media_raf = 0
cont_raf = 0
int_totale = 0
dur_raf = 0 """

# Def. variabili per conteggio raffiche nelle finestre temporali
media_raf = np.zeros(int(np.round(n_rid/durata_int)))
cont_raf = np.zeros(int(np.round(n_rid/durata_int)))
int_totale = np.zeros(int(np.round(n_rid/durata_int)))
dur_raf = np.zeros(int(np.round(n_rid/durata_int)))

param_1 = 1.3
param_2 = 0.85

i=5
j=2
interv = 0 # indice per l'intervallo
fine_raff_prec = 0
while i<n_rid:
    if V[i]>param_1*np.mean(V[i-5:i-4]) and V[i]>1:
        fine_raff_prec=j
        j=i
        while V[j]>param_2*np.mean(V[j-3:j-1]) and j<n:
            j=j+1
        
        # Mostra intensità vento da fine raffica precedente a fine raffica successiva
        plt_pyplot.scatter(np.arange(fine_raff_prec,j+1,1),V[fine_raff_prec:j+1])
        plt_pyplot.xlabel('Tempo')
        plt_pyplot.ylabel('Intensità vento [km/h]')
        
        # Contrassegna inizio raffica nel grafico (puntino colorato)
        plt_pyplot.scatter(i-3, V[i-3])
        plt_pyplot.show()
        
        # aggiorno variabili
        """media_raf=np.mean(V[i-3:j]) # entrano nella stat anche i 3s prima
        cont_raf+=1 
        int_totale+=media_raf
        dur_raf+=j-i-3
        i=j  # Riparto da dove è finita l'ultima raffica"""
        
        # aggiorno variabili
        media_raf=np.mean(V[i-3:j]) 
        cont_raf[interv]+=1
        int_totale[interv]+=media_raf
        dur_raf[interv]+=j-i-3
        i=j
        
    i+=1 #incremento i
    if i-durata_int*interv==durata_int:
            interv+=1 # passaggio ad un nuovo intervallo
    
# Calcola intensità e durata media raffica per tutto il file    
"""if cont_raf>=1:
    int_totale_med = int_totale/cont_raf
    dur_raf_med = dur_raf/cont_raf;
    print('Intensità media raf: ' + str(int_totale_med))
    print('Durata media raf ' + str(dur_raf_med))    
    print('Contatore raffiche: ' + str(cont_raf))"""

# Calcola intensità e durata media raffica per le finestre temporali   
interv=0   
while interv<int(n_rid/durata_int):
    if cont_raf[interv]>=1:
        int_totale[interv]=int_totale[interv]/cont_raf[interv]
        dur_raf[interv]=dur_raf[interv]/cont_raf[interv]
        print('Intensità media raffiche nel intervallo ' + str(interv) + ': ' + str(int_totale[interv]))
        print('Durata media raffiche nel intervallo ' + str(interv) + ': ' + str(dur_raf[interv]))    
        print('Contatore raffiche nel intervallo ' + str(interv) + ': ' + str(int(cont_raf[interv])))    
    
    interv+=1 # passo all'intervallo successivo 
                

                