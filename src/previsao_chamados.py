import pandas as pd
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

def previsao_volume_chamados(df: pd.DataFrame):
    """Previsão de volume de chamados por semana (baseado na coluna 'Iniciado em')."""
    
    # Remover espaços extras nas colunas
    df.columns = df.columns.str.strip()

    # Verifica se a coluna 'Iniciado em' existe
    if 'Iniciado em' not in df.columns:
        print("Coluna 'Iniciado em' não encontrada no DataFrame. Colunas disponíveis:", df.columns)
        return
    
    # Converte a coluna 'Iniciado em' para o formato de data (formato dd/mm/yyyy hh:mm)
    df['Iniciado em'] = pd.to_datetime(df['Iniciado em'], format='%d/%m/%Y %H:%M', errors='coerce')

    # Verifica se houve erro na conversão (por exemplo, valores inválidos)
    if df['Iniciado em'].isnull().any():
        print("Existem valores inválidos na coluna 'Iniciado em'. Verifique os dados.")
        return
    
    # Extração da semana do ano
    df['Semana'] = df['Iniciado em'].dt.isocalendar().week
    print("\n🔹 Previsão de volume de chamados por semana:")
    chamados_por_semana = df['Semana'].value_counts().sort_index()
    print(chamados_por_semana)
    
    # Gráfico (se necessário, adapte conforme os requisitos)
    plt.figure(figsize=(10, 6))
    ax = sns.lineplot(x=chamados_por_semana.index, y=chamados_por_semana.values, marker='o')
    
    # Adicionando anotações de todos os valores exatos nos pontos
    for i, value in enumerate(chamados_por_semana.values):
        ax.text(chamados_por_semana.index[i], value, str(value), 
                color='black', ha='center', va='bottom', fontsize=10)
    
    plt.title('Volume de Chamados por Semana')
    plt.xlabel('Semana do Ano')
    plt.ylabel('Quantidade de Chamados')
    plt.tight_layout()
    plt.savefig('graficos/volume_chamados_por_semana.png')  # Salvar o gráfico
    plt.show()

# Carregar os dados (ajuste o caminho do arquivo CSV conforme necessário)
df_jan_mar = pd.read_csv('dados_tiflux/janeiro_março.csv', delimiter=';', encoding='utf-8')
df_mar_abr = pd.read_csv('dados_tiflux/março_abril.csv', delimiter=';', encoding='utf-8')

# Chamar a função para gerar o gráfico
previsao_volume_chamados(df_jan_mar)
previsao_volume_chamados(df_mar_abr)
