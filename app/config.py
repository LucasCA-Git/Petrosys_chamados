import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPHS_DIR = os.path.join(BASE_DIR,'graficos')
DATA_DIR = os.path.join(BASE_DIR, 'dados_tiflux')  # Pasta com os Excel originais

# Garante que as pastas existam
os.makedirs(GRAPHS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)