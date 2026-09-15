from flask import Flask, render_template, send_file
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import io

import requests 
matplotlib.use('Agg')  # Use the 'Agg' backend for non-GUI environments
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")



@app.route("/grafico")
def grafics():
    # Load the CSV file
    df = pd.read_csv('aziende.csv')
    df["consumo_kwh"] = df["consumo_kwh"].astype(float)  # Ensure the column is float
    for i, riga in df.iterrows():
        response = requests.get(
            "https://api.emissions.dev/v1/electricity/emissions",
            params={"kwh": riga["consumo_kwh"], "country": riga["paese"]},
            headers={"Authorization": "Bearer em_live_pa7FMfXEgfDdWV3ptzasYGSQ5sVy7d5QTv8Ei3"},
            timeout=10
        )
        if response.status_code == 200:
            df.at[i, "consumo_kwh"] = response.json()["data"]["attributes"]["emissions"]["co2e"]

    df.to_csv('aziende.csv', index=False)



    # Create a plot
    plt.figure(figsize=(10, 6))
    plt.plot(df['azienda'][:2], df['consumo_kwh'], marker='o')
    plt.title('Grafico del consumo di energia delle aziende')
    plt.xlabel('Aziende')
    plt.ylabel('Consumo (kWh)')
    plt.grid()

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)