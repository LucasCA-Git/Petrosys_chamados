import os
from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).parent.parent.resolve()

# Diretório para salvar os gráficos
GRAPHS_DIR = BASE_DIR / 'app' / 'static' / 'graficos'

# Diretório para salvar os dados
DATA_DIR = BASE_DIR / 'dados_tiflux'

# Cria os diretórios, se não existirem
GRAPHS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)