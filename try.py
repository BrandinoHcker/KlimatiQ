# Test di verifica delle librerie
try:
    import pandas as pd
    import requests
    import matplotlib.pyplot as plt
    import openpyxl
    print("Tutte le librerie sono installate correttamente! Puoi iniziare.")
except ImportError as e:
    print(f"Manca ancora qualcosa. Errore: {e}")

import sys
import subprocess

subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
