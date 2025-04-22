import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def chamados_por_temporalidade(df: pd.DataFrame):
    """Exibe gráficos de chamados por dia da semana e por hora do dia com numeração exata."""
    
    # Chamados por dia da semana
    chamados_por_dia = df['Dia_Semana'].value_counts().sort_index()
    print("\n🔹 Chamados por dia da semana:")
    print(chamados_por_dia)

    # Gráfico de chamados por dia da semana
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=chamados_por_dia.index, y=chamados_por_dia.values, marker='o')
    plt.title('Chamados por dia da semana')
    plt.xlabel('Dia da Semana')
    plt.ylabel('Quantidade de Chamados')
    plt.xticks(rotation=45)

    # Adicionando os valores no gráfico
    for i, v in enumerate(chamados_por_dia.values):
        plt.text(i, v + 0.1, str(v), ha='center', va='bottom', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('graficos/chamados_por_dia.png')  # Salvar o gráfico
    plt.show()

    # Chamados por hora do dia
    chamados_por_hora = df['Hora'].value_counts().sort_index()
    print("\n🔹 Chamados por hora do dia:")
    print(chamados_por_hora)

    # Gráfico de chamados por hora do dia
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=chamados_por_hora.index, y=chamados_por_hora.values, marker='o')
    plt.title('Chamados por hora do dia')
    plt.xlabel('Hora do Dia')
    plt.ylabel('Quantidade de Chamados')
    plt.xticks(rotation=45)

    # Adicionando os valores no gráfico para cada hora
    for i, v in enumerate(chamados_por_hora.values):
        plt.text(i, v + 0.1, str(v), ha='center', va='bottom', fontsize=11)

    plt.tight_layout()
    plt.savefig('graficos/chamados_por_hora.png')  # Salvar o gráfico
    plt.show()
