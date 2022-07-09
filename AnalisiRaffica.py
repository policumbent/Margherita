#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 18:06:19 2022

@author: felixackermann
"""

import csv
import numpy as np
import matplotlib.pylab as plt 
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
V = np.float_([M[i][3] for i in range(n)]) # non posso usare : per array multidimensionale

t = np.zeros((int(np.round(n/900)),5)) # per caratterizzare intervalli di 15min
bool = True


i=1
while bool:
    t[i-1][0] = np.amax(V[900*(i-1):900*i])
    t[i-1][1] = np.amin(V[900*(i-1):900*i])
    t[i-1][2] = np.mean(V[900*(i-1):900*i])
    t[i-1][3] = st.median(V[900*(i-1):900*i]) # da aggiustare, così scritto non funziona
    t[i-1][4] = np.sqrt(np.mean(V[900*(i-1):900*i]))
    
    if n-900*i >= 900:
        i += 1
    else:
        bool = False
        
        
i=4
j=2
media_raf = 0
cont_raf = 0
int_totale = 0
dur_raf = 0
param_1 = 1.2
param_2 = 0.8
fine_raff_prec = 0

while i<n:
    if V[i]>param_1*np.mean(V[i-2:i-1]) and V[i]>0.5:
        fine_raff_prec=j
        j=i
        while V[j]>param_2*np.mean(V[j-3:j-1]) and j<n:
            j=j+1
        
        plt.plot(np.arange(fine_raff_prec,j+1,1),V[fine_raff_prec:j+1])
        plt.xlabel('Tempo')
        plt.ylabel('Intensità vento [km/h]')            
        
        media_raf = np.mean(V[i:j])
        cont_raf+=1 
        int_totale+=media_raf
        dur_raf+=j-i
        i=j  # Riparto da dove è finita l'ultia raffica
    
    i+=1 #incremento i
    
if cont_raf>=1:
    int_totale_med = int_totale/cont_raf
    dur_raf_med = dur_raf/cont_raf;
    print('Intensità media raf: ' + str(int_totale_med))
    print('Durata media raf ' + str(dur_raf_med))    
    print('Contatore raffiche: ' + str(cont_raf))
            

                

                