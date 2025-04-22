import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def resumo_geral(df: pd.DataFrame):
    """Exibe um resumo geral dos dados carregados."""
    
    # Ordenar a coluna 'Dia_Semana' com a sequência correta
    dias_da_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['Dia_Semana'] = pd.Categorical(df['Dia_Semana'], categories=dias_da_semana, ordered=True)

    # Chamados por dia da semana
    chamados_por_dia = df['Dia_Semana'].value_counts().sort_index()

    print("🔹 Chamados por dia da semana:")
    print(chamados_por_dia)

    # Gráfico de chamados por dia da semana (com valores exatos)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=chamados_por_dia.index, y=chamados_por_dia.values, palette='viridis')
    for i, v in enumerate(chamados_por_dia.values):
        plt.text(i, v + max(chamados_por_dia.values)*0.01, str(v), ha='center', va='bottom', fontsize=11)
    plt.title('Chamados por dia da semana')
    plt.xlabel('Dia da Semana')
    plt.ylabel('Quantidade de Chamados')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('graficos/chamados_por_dia.png')
    plt.show()

    # Chamados por hora do dia
    print("\n🔹 Chamados por hora do dia:")
    chamados_por_hora = df['Hora'].value_counts().sort_index()
    print(chamados_por_hora)

    # Gráfico de chamados por hora do dia (com valores exatos)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=chamados_por_hora.index, y=chamados_por_hora.values, palette='Blues')
    for i, v in enumerate(chamados_por_hora.values):
        plt.text(i, v + max(chamados_por_hora.values)*0.01, str(v), ha='center', va='bottom', fontsize=11)
    plt.title('Chamados por hora do dia')
    plt.xlabel('Hora do Dia')
    plt.ylabel('Quantidade de Chamados')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('graficos/chamados_por_hora.png')
    plt.show()

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
