import os
import pandas as pd
from pandas.api.types import CategoricalDtype
import matplotlib.pyplot as plt
import seaborn as sns

def gerar_grafico(dados, titulo, xlabel, ylabel, caminho_arquivo, tipo='bar', palette=None):
    """Gera e salva um gráfico com base nos dados fornecidos."""
    plt.figure(figsize=(10, 6))
    if tipo == 'line':
        sns.lineplot(x=dados.index, y=dados.values, marker='o')
    elif tipo == 'bar':
        sns.barplot(x=dados.index, y=dados.values, palette=palette)
    else:
        raise ValueError("Tipo de gráfico inválido. Use 'line' ou 'bar'.")

    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)

    # Adicionando os valores no gráfico
    for i, v in enumerate(dados.values):
        plt.text(i, v + max(dados.values) * 0.01, str(v), ha='center', va='bottom', fontsize=11)

    plt.tight_layout()
    plt.savefig(caminho_arquivo)
    plt.show()

def analise_temporal(df: pd.DataFrame, periodo: str):
    """Realiza análises temporais (mensal e por dia da semana) e gera gráficos."""
    # Definir a ordem dos dias da semana
    ordem_dias = CategoricalDtype(
        categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        ordered=True
    )
    df['Dia_Semana'] = df['Dia_Semana'].astype(ordem_dias)

    # Chamados por dia da semana
    chamados_por_dia = df['Dia_Semana'].value_counts().sort_index()
    gerar_grafico(
        dados=chamados_por_dia,
        titulo=f'Chamados por dia da semana ({periodo})',
        xlabel='Dia da Semana',
        ylabel='Quantidade de Chamados',
        caminho_arquivo=f'graficos/chamados_por_dia_{periodo}.png',
        tipo='bar'
    )

    # Chamados por hora do dia
    chamados_por_hora = df['Hora'].value_counts().sort_index()
    gerar_grafico(
        dados=chamados_por_hora,
        titulo=f'Chamados por hora do dia ({periodo})',
        xlabel='Hora do Dia',
        ylabel='Quantidade de Chamados',
        caminho_arquivo=f'graficos/chamados_por_hora_{periodo}.png',
        tipo='bar'
    )

    # Chamados por mês
    df['Mes'] = pd.to_datetime(df['Iniciado em'], errors='coerce').dt.month
    chamados_por_mes = df['Mes'].value_counts().sort_index()
    gerar_grafico(
        dados=chamados_por_mes,
        titulo=f'Chamados por mês ({periodo})',
        xlabel='Mês',
        ylabel='Quantidade de Chamados',
        caminho_arquivo=f'graficos/chamados_por_mes_{periodo}.png',
        tipo='bar'
    )

def solicitantes_mais_chamaram(df: pd.DataFrame, periodo: str):
    """Exibe os clientes que mais chamaram."""
    clientes = df['Cliente'].value_counts().sort_values(ascending=False)
    gerar_grafico(
        dados=clientes.head(10),  # Exibir os 10 principais clientes
        titulo=f'Clientes que mais chamaram ({periodo})',
        xlabel='Cliente',
        ylabel='Quantidade de Chamados',
        caminho_arquivo=f'graficos/clientes_mais_chamaram_{periodo}.png',
        tipo='bar'
    )

def main():
    """Função principal para executar o programa."""
    # Caminhos dos arquivos CSV
    caminho_janeiro_marco = 'dados_tiflux/janeiro_março.csv'
    caminho_marco_abril = 'dados_tiflux/março_abril.csv'

    # Carregar os arquivos CSV
    df_janeiro_marco = pd.read_csv(caminho_janeiro_marco, delimiter=';', encoding='utf-8')
    df_marco_abril = pd.read_csv(caminho_marco_abril, delimiter=';', encoding='utf-8')

    # Tratar datas e colunas
    for df in [df_janeiro_marco, df_marco_abril]:
        df['Dia_Semana'] = pd.to_datetime(df['Iniciado em'], errors='coerce').dt.day_name()
        df['Hora'] = pd.to_datetime(df['Iniciado em'], errors='coerce').dt.hour

    # Análises separadas para Janeiro-Março
    print("\n=== Análise para Janeiro-Março ===")
    analise_temporal(df_janeiro_marco, 'Janeiro-Março')
    solicitantes_mais_chamaram(df_janeiro_marco, 'Janeiro-Março')

    # Análises separadas para Março-Abril
    print("\n=== Análise para Março-Abril ===")
    analise_temporal(df_marco_abril, 'Março-Abril')
    solicitantes_mais_chamaram(df_marco_abril, 'Março-Abril')

    # Combinar os dois DataFrames
    df_combinado = pd.concat([df_janeiro_marco, df_marco_abril], ignore_index=True)

    # Análise combinada para Janeiro-Abril
    print("\n=== Análise para Janeiro-Abril (Combinado) ===")
    analise_temporal(df_combinado, 'Janeiro-Abril')
    solicitantes_mais_chamaram(df_combinado, 'Janeiro-Abril')

if __name__ == "__main__":
    main()