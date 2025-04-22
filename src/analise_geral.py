import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def resumo_geral(df: pd.DataFrame):
    """Exibe um resumo geral dos dados carregados."""
    
    # Chamados por dia da semana
    print("🔹 Chamados por dia da semana:")
    print(df['Dia_Semana'].value_counts())

    # Chamados por hora do dia
    print("\n🔹 Chamados por hora do dia:")
    print(df['Hora'].value_counts().sort_index())

    # Percentual de chamados com avaliação
    if 'Avaliação' in df.columns:
        avaliados = df['Avaliação'].notna().sum()
        total = len(df)
        percentual = (avaliados / total) * 100
        print(f"\n🔹 Percentual de chamados com avaliação:")
        print(f"{percentual:.2f}% ({avaliados}/{total})")
    else:
        print("Coluna 'Avaliação' não encontrada.")

    # Tempo médio até finalização
    if 'Finalizado_em' in df.columns and 'Iniciado_em' in df.columns:
        df['Iniciado_em'] = pd.to_datetime(df['Iniciado_em'], errors='coerce')
        df['Finalizado_em'] = pd.to_datetime(df['Finalizado_em'], errors='coerce')
        tempo_medio = df['Finalizado_em'] - df['Iniciado_em']
        print(f"\n🔹 Tempo médio até finalização:")
        print(f"Tempo médio: {tempo_medio.mean()}")
    else:
        print("Colunas 'Iniciado_em' ou 'Finalizado_em' não encontradas.")
    
    # Gerar gráficos
    # Gráfico de chamados por dia da semana
    chamados_por_dia = df['Dia_Semana'].value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=chamados_por_dia.index, y=chamados_por_dia.values, palette='viridis')
    plt.title('Chamados por dia da semana')
    plt.xlabel('Dia da Semana')
    plt.ylabel('Quantidade de Chamados')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('graficos/chamados_por_dia.png')  # Salvar o gráfico
    plt.show()

    # Gráfico de chamados por hora do dia
    chamados_por_hora = df['Hora'].value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=chamados_por_hora.index, y=chamados_por_hora.values, palette='Blues')
    plt.title('Chamados por hora do dia')
    plt.xlabel('Hora do Dia')
    plt.ylabel('Quantidade de Chamados')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('graficos/chamados_por_hora.png')  # Salvar o gráfico
    plt.show()
