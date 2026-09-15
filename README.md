# KlimatiQ

Progetto KlimatiQ — Calcolo emissioni CO2
Struttura cartelle
KlimatiQ/
├── aziende.csv              # Dataset aziende (paese, settore, consumo kWh)
├── script/
│   ├── ambient_impact.py    # Chiama le API emissions.dev e calcola CO2
│   └── grafici_emissioni.py # Genera i grafici a partire dai risultati
├── grafici/
│   ├── grafico_totale.png
│   ├── grafico_composizione.png
│   └── grafico_torta.png
└── config/
    └── .env.example         # Modello per la chiave API (da rinominare in .env)

Come usarlo
Copia config/.env.example nella cartella script/, rinominalo in .env e inserisci la tua chiave: EMISSIONS_API_KEY=em_live_xxxxx
Installa le dipendenze: pip install pandas requests python-dotenv matplotlib
Esegui python script/ambient_impact.py per calcolare le emissioni
Esegui python script/grafici_emissioni.py per generare i grafici
