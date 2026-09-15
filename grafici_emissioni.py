"""
Genera grafici a partire dai dati di emissioni CO2 calcolati per ogni azienda.
Da eseguire DOPO ambient_impact.py (o integrato con esso), usando lo stesso
DataFrame con le colonne: azienda, CO2_Elettricita_kg, CO2_Carburante_kg,
CO2_Viaggio_kg, CO2_Merci_kg, CO2_Totale_kg.
"""

import matplotlib.pyplot as plt
import pandas as pd


def crea_grafico_totale_per_azienda(df, salva_come="grafico_totale.png"):
    """Grafico a barre: emissioni totali (kg CO2) per azienda."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(df["azienda"], df["CO2_Totale_kg"], color="#0D83CC")
    ax.set_title("Emissioni CO2 totali per azienda")
    ax.set_xlabel("Azienda")
    ax.set_ylabel("CO2 totale (kg)")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.tight_layout()
    fig.savefig(salva_come, dpi=150)
    plt.close(fig)
    print(f"Salvato: {salva_come}")


def crea_grafico_composizione(df, salva_come="grafico_composizione.png"):
    """Grafico a barre impilate: composizione delle emissioni per categoria, per azienda."""
    categorie = [
        ("CO2_Elettricita_kg", "Elettricità"),
        ("CO2_Carburante_kg", "Carburante/Gas"),
        ("CO2_Viaggio_kg", "Viaggi"),
        ("CO2_Merci_kg", "Merci"),
    ]
    colori = ["#1976D2", "#F9A825", "#8E24AA", "#D84315"]

    fig, ax = plt.subplots(figsize=(9, 6))
    base = [0] * len(df)
    for (colonna, etichetta), colore in zip(categorie, colori):
        if colonna in df.columns:
            valori = df[colonna].fillna(0)
            ax.bar(df["azienda"], valori, bottom=base, label=etichetta, color=colore)
            base = [b + v for b, v in zip(base, valori)]

    ax.set_title("Composizione delle emissioni CO2 per azienda")
    ax.set_xlabel("Azienda")
    ax.set_ylabel("CO2 (kg)")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.tight_layout()
    fig.savefig(salva_come, dpi=150)
    plt.close(fig)
    print(f"Salvato: {salva_come}")


def crea_grafico_torta(df, salva_come="grafico_torta.png"):
    """Grafico a torta: quota di emissioni totali per azienda."""
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        df["CO2_Totale_kg"],
        labels=df["azienda"],
        autopct="%1.1f%%",
        colors=["#2E7D32", "#1976D2", "#F9A825", "#8E24AA", "#D84315"][: len(df)],
    )
    ax.set_title("Quota di emissioni CO2 totali per azienda")
    fig.tight_layout()
    fig.savefig(salva_come, dpi=150)
    plt.close(fig)
    print(f"Salvato: {salva_come}")


if __name__ == "__main__":
    # --- ESEMPIO DI USO ---
    # In produzione, sostituisci questo blocco con l'import del DataFrame
    # reale prodotto da ambient_impact.py, es:
    #
    #   from ambient_impact import df
    #
    # oppure carica un CSV già salvato con i risultati:
    #
    #   df = pd.read_csv("risultati_emissioni.csv")

    df_esempio = pd.DataFrame(
        {
            "azienda": ["MilanTech", "BerlinAuto", "NYCloud"],
            "CO2_Elettricita_kg": [6500, 42000, 55000],
            "CO2_Carburante_kg": [1600, 8000, 4200],
            "CO2_Viaggio_kg": [180, 45, 950],
            "CO2_Merci_kg": [320, 1100, 8600],
        }
    )
    df_esempio["CO2_Totale_kg"] = (
        df_esempio["CO2_Elettricita_kg"]
        + df_esempio["CO2_Carburante_kg"]
        + df_esempio["CO2_Viaggio_kg"]
        + df_esempio["CO2_Merci_kg"]
    )

    crea_grafico_totale_per_azienda(df_esempio)
    crea_grafico_composizione(df_esempio)
    crea_grafico_torta(df_esempio)
