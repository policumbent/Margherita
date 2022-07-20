# Margherita
Analisi Raffiche Vento

Il codice analisiRaff identifica le raffiche, ne determina la durata e l'intensità media. Viene utilizzato un filtro di media mobile per regolarizzare il dato, evitando così raffiche di durata troppo corta.

Scelte parametri: 
- più è alto param_1, più è forte la condizione per fare iniziare la raffica,
- più param_2 è vicino al valore 1, meno è forte la condizione per fare terminare la raffica.

Valori consigliati per i parametri: param_1 = 1.3, param_2 = 0.85

Mod 20/7/2022: 
per evitare che piccoli incrementi rendano più difficile l'identificazione della raffica, per la condizione su inizio raffica si confronta il valore attuale con una media di due valori registrati a distanza di 5s in precedenza. Inoltre: per le statistiche l'inizio della raffica è anticipato di 3s perché l'identificazione dell'inizio della raffica avviene leggermente in ritardo. 
