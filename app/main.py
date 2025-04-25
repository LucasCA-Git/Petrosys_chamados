import os
import pandas as pd
from app.config import DATA_DIR

# Função para consolidar os dados de todos os arquivos mensais
def consolidar_dados_mensais(diretorio_dados):
    """
    Consolida os dados de todos os arquivos mensais em um único DataFrame.
    """
    arquivos = [f for f in os.listdir(diretorio_dados) if f.endswith('.xlsx')]
    df_total = pd.DataFrame()

    for arquivo in arquivos:
        caminho_arquivo = os.path.join(diretorio_dados, arquivo)
        df_mes = pd.read_excel(caminho_arquivo)
        df_total = pd.concat([df_total, df_mes], ignore_index=True)

    return df_total

# Função principal para consolidar dados e gerar relatórios
def processar_dados():
    """
    Consolida os dados e chama as funções de geração de gráficos e relatórios.
    """
    from app.relatorios import gerar_relatorios_consolidados  # Importação local para evitar ciclos
    df_total = consolidar_dados_mensais(DATA_DIR)
    gerar_relatorios_consolidados(df_total)