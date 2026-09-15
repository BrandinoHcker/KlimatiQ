import os
import pandas as pd
import requests
from dotenv import load_dotenv
import matplotlib.pyplot as plt

# --- CONFIGURAZIONE API ---
ELECTRICITY_URL = "https://api.emissions.dev/v1/electricity/emissions"
FUEL_URL = "https://api.emissions.dev/v1/fuel/emissions"
TRAVEL_URL = "https://api.emissions.dev/v1/travel/emissions"
FREIGHT_URL = "https://api.emissions.dev/v1/freight/emissions"

# La chiave viene letta da un file .env nella stessa cartella dello script
# (vedi istruzioni per crearlo prima di eseguire).
load_dotenv()
API_KEY = os.environ.get('em_live_pa7FMfXEgfDdWV3ptzasYGSQ5sVy7d5QTv8Ei3')

if not API_KEY:
    raise RuntimeError(
        "Variabile d'ambiente EMISSIONS_API_KEY non impostata. "
        "Imposta la chiave prima di eseguire lo script (vedi commento sopra)."
    )

HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def calcola_co2_elettricita(kwh, codice_paese="US"):
    """
    Interroga l'API emissions.dev per calcolare l'impatto CO2
    in base al mix energetico del paese specificato.
    """
    params = {
        "kwh": kwh,
        "country": codice_paese.upper(),  # Es. 'US', 'IT', 'DE'
    }

    try:
        response = requests.get(ELECTRICITY_URL, params=params, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            data = response.json()
            # I dati utili sono annidati sotto data -> attributes -> emissions
            return data["data"]["attributes"]["emissions"]["co2e"]
        else:
            print(f"Errore del server ({response.status_code}): {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Errore di rete: {e}")
        return None


def calcola_co2_carburante(fuel_type, amount, unit=None):
    """
    Interroga l'API emissions.dev per calcolare le emissioni Scope 1
    da combustione diretta di carburante (gas naturale, diesel, GPL, ecc.).

    fuel_type: es. 'natural_gas', 'diesel', 'lpg', 'petrol', 'cng',
               'kerosene', 'fuel_oil', 'coal_industrial', ...
    amount: quantità consumata
    unit: unità di misura (es. 'kwh', 'litre', 'kg', 'therm', 'm3').
          Se omessa, l'API usa l'unità predefinita per quel carburante.
    """
    params = {
        "fuel_type": fuel_type,
        "amount": amount,
    }
    if unit:
        params["unit"] = unit

    try:
        response = requests.get(FUEL_URL, params=params, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return data["data"]["attributes"]["emissions"]["co2e"]
        else:
            print(f"Errore del server ({response.status_code}): {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Errore di rete: {e}")
        return None


def calcola_co2_viaggio(
    origine_paese, origine_citta, destinazione_paese, destinazione_citta,
    modo_trasporto="flight", classe_cabina=None
):
    """
    Interroga l'API emissions.dev per calcolare le emissioni di un viaggio.

    modo_trasporto: 'flight', 'rail', 'car', 'bus', 'ferry', 'taxi'
    classe_cabina: solo per i voli: 'economy', 'business', 'first' (opzionale)
    """
    params = {
        "origin_country": origine_paese,
        "origin_location": origine_citta,
        "destination_country": destinazione_paese,
        "destination_location": destinazione_citta,
        "transport_mode": modo_trasporto,
    }
    if classe_cabina:
        params["cabin_class"] = classe_cabina

    try:
        response = requests.get(TRAVEL_URL, params=params, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return data["data"]["attributes"]["emissions"]["co2e"]
        else:
            print(f"Errore del server ({response.status_code}): {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Errore di rete: {e}")
        return None


def calcola_co2_merci(
    origine_paese, origine_citta, destinazione_paese, destinazione_citta,
    peso_kg, modo_trasporto="road", tipo_veicolo=None, fonte_carburante=None,
    refrigerato=False
):
    """
    Interroga l'API emissions.dev per calcolare le emissioni di una spedizione merci.

    modo_trasporto: 'road', 'rail', 'sea', 'air'
    tipo_veicolo (solo road): 'small_van', 'van', 'truck', 'hgv', 'articulated', 'average'
    fonte_carburante (solo road): 'diesel', 'petrol', 'electric', 'lng', 'cng', 'hvo', ...
    """
    params = {
        "origin_country": origine_paese,
        "origin_location": origine_citta,
        "destination_country": destinazione_paese,
        "destination_location": destinazione_citta,
        "weight": peso_kg,
        "transport_mode": modo_trasporto,
    }
    if tipo_veicolo:
        params["vehicle_type"] = tipo_veicolo
    if fonte_carburante:
        params["fuel_source"] = fonte_carburante
    if refrigerato:
        params["refrigerated"] = "true"

    try:
        response = requests.get(FREIGHT_URL, params=params, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return data["data"]["attributes"]["emissions"]["co2e"]
        else:
            print(f"Errore del server ({response.status_code}): {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Errore di rete: {e}")
        return None


# --- SIMULAZIONE SUL TUO DATASET DI AZIENDE ---
# Ogni azienda ha: elettricità, carburante/gas, un viaggio di lavoro, una spedizione merci
dati_aziende = [
    {
        "azienda": "MilanTech", "paese": "IT", "citta_sede": "Milan", "kwh": 15000,
        "fuel_type": "natural_gas", "fuel_amount": 8000, "fuel_unit": "kwh",
        "viaggio_dest_paese": "DE", "viaggio_dest_citta": "Berlin", "viaggio_modo": "flight",
        "merci_dest_paese": "DE", "merci_dest_citta": "Berlin", "merci_peso_kg": 2500, "merci_modo": "road",
    },
    {
        "azienda": "BerlinAuto", "paese": "DE", "citta_sede": "Berlin", "kwh": 85000,
        "fuel_type": "diesel", "fuel_amount": 3000, "fuel_unit": "litre",
        "viaggio_dest_paese": "IT", "viaggio_dest_citta": "Milan", "viaggio_modo": "rail",
        "merci_dest_paese": "FR", "merci_dest_citta": "Paris", "merci_peso_kg": 5000, "merci_modo": "road",
    },
    {
        "azienda": "NYCloud", "paese": "US", "citta_sede": "New York", "kwh": 120000,
        "fuel_type": "natural_gas", "fuel_amount": 20000, "fuel_unit": "kwh",
        "viaggio_dest_paese": "US", "viaggio_dest_citta": "San Francisco", "viaggio_modo": "flight",
        "merci_dest_paese": "CN", "merci_dest_citta": "Shanghai", "merci_peso_kg": 20000, "merci_modo": "sea",
    },
]

df = pd.DataFrame(dati_aziende)

print("Interrogazione dell'API per ogni azienda...")

df["CO2_Elettricita_kg"] = df.apply(
    lambda riga: calcola_co2_elettricita(riga["kwh"], riga["paese"]), axis=1
)

df["CO2_Carburante_kg"] = df.apply(
    lambda riga: calcola_co2_carburante(
        riga["fuel_type"], riga["fuel_amount"], riga["fuel_unit"]
    ),
    axis=1,
)

df["CO2_Viaggio_kg"] = df.apply(
    lambda riga: calcola_co2_viaggio(
        riga["paese"], riga["citta_sede"],
        riga["viaggio_dest_paese"], riga["viaggio_dest_citta"],
        riga["viaggio_modo"],
    ),
    axis=1,
)

plt.xlabel("Azienda")
plt.ylabel("CO₂e (kg)")

plt.xticks(rotation=20)

# Mostra il valore sopra ogni barra
for i, valore in enumerate(df["CO2_Totale_kg"]):
    plt.text(
        i,
        valore,
        f"{valore:,.0f}",
        ha="center",
        va="bottom",
    )


df["CO2_Merci_kg"] = df.apply(
    lambda riga: calcola_co2_merci(
        riga["paese"], riga["citta_sede"],
        riga["merci_dest_paese"], riga["merci_dest_citta"],
        riga["merci_peso_kg"], riga["merci_modo"],
    ),
    axis=1,
)

df["CO2_Totale_kg"] = (
    df["CO2_Elettricita_kg"]
    + df["CO2_Carburante_kg"]
    + df["CO2_Viaggio_kg"]
    + df["CO2_Merci_kg"]
)







print("\n--- RISULTATO FINALE ---")
print(df)
