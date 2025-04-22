import pandas as pd
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

def previsao_volume_chamados(df: pd.DataFrame):
    """Previsão de volume de chamados por semana (baseado na coluna 'Iniciado em')."""
    
    # Remover espaços extras nas colunas
    df.columns = df.columns.str.strip()

    # Verifica se a coluna 'Iniciado em' existe
    if 'Iniciado_em' not in df.columns:
        print("Coluna 'Iniciado_em' não encontrada no DataFrame.")
        return

    # Converte para datetime
    df['Iniciado_em'] = pd.to_datetime(df['Iniciado_em'], errors='coerce')
    df['Semana'] = df['Iniciado_em'].dt.isocalendar().week

    # Contagem de chamados por semana
    chamados_por_semana = df['Semana'].value_counts().sort_index()
    print(f"\n🔹 Chamados por semana:")
    print(chamados_por_semana)

    # Gráfico de chamados por semana
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=chamados_por_semana.index, y=chamados_por_semana.values, marker='o')
    plt.title('Volume de Chamados por Semana')
    plt.xlabel('Semana')
    plt.ylabel('Quantidade de Chamados')
    plt.xticks(rotation=45)

    # Adicionando os valores no gráfico
    for i, v in enumerate(chamados_por_semana.values):
        plt.text(i, v + 0.1, str(v), ha='center', va='bottom', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('graficos/previsao_volume_chamados.png')  # Salvar o gráfico
    plt.show()
