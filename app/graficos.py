import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from app.config import GRAPHS_DIR

def gerar_grafico(dados, titulo, xlabel, ylabel, caminho_arquivo, tipo='bar', horizontal=False, palette='Blues'):
    """
    Gera gráficos de barras ou linhas com opções de orientação horizontal.
    """
    plt.figure(figsize=(16, 8))
    if tipo == 'bar':
        if horizontal:
            ax = sns.barplot(y=dados.index, x=dados.values, palette=palette, orient='h')
            for p in ax.patches:
                ax.text(p.get_width() + 0.5, p.get_y() + p.get_height() / 2, f'{int(p.get_width())}', va='center')
        else:
            ax = sns.barplot(x=dados.index, y=dados.values, palette=palette)
            for p in ax.patches:
                ax.text(p.get_x() + p.get_width() / 2, p.get_height() + 0.5, f'{int(p.get_height())}', ha='center')
    elif tipo == 'line':
        sns.lineplot(x=dados.index, y=dados.values, marker='o', linewidth=2.5)
    else:
        raise ValueError("Tipo de gráfico inválido. Use 'bar' ou 'line'.")

    plt.title(titulo, fontsize=14, pad=20)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.tight_layout()
    plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
    plt.close()

def gerar_grafico_item_catalogo_anual(df):
    """
    Gera gráfico consolidado de itens do catálogo.
    """
    if 'Item do Catálogo' in df.columns:
        itens_catalogo = df['Item do Catálogo'].value_counts().head(15)
        caminho = os.path.join(GRAPHS_DIR, 'itens_catalogo_total_anual.png')
        gerar_grafico(
            dados=itens_catalogo,
            titulo='Top 15 Problemas mais recorrentes',
            xlabel='Quantidade',
            ylabel='Item do Catálogo',
            caminho_arquivo=caminho,
            horizontal=True,
            palette='Blues_r'
        )

def gerar_grafico_chamados_por_mes(df):
    """
    Gera gráfico consolidado de chamados por mês.
    """
    df['Mes'] = pd.to_datetime(df['Iniciado em'], errors='coerce').dt.strftime('%B')
    chamados_por_mes = df['Mes'].value_counts().sort_index()
    caminho = os.path.join(GRAPHS_DIR, 'chamados_por_mes.png')
    gerar_grafico(
        dados=chamados_por_mes,
        titulo='Chamados por Mês',
        xlabel='Mês',
        ylabel='Quantidade de Chamados',
        caminho_arquivo=caminho,
        horizontal=False,
        palette='Blues'
    )

def gerar_grafico_chamados_por_dia(df):
    """
    Gera gráfico consolidado de chamados por dia da semana.
    """
    df['Dia_Semana'] = pd.to_datetime(df['Iniciado em'], errors='coerce').dt.day_name()
    ordem_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    chamados_por_dia = df['Dia_Semana'].value_counts().reindex(ordem_dias, fill_value=0)
    caminho = os.path.join(GRAPHS_DIR, 'chamados_por_dia.png')
    gerar_grafico(
        dados=chamados_por_dia,
        titulo='Chamados por Dia da Semana',
        xlabel='Dia da Semana',
        ylabel='Quantidade de Chamados',
        caminho_arquivo=caminho,
        horizontal=False,
        palette='Blues'
    )

def gerar_grafico_chamados_por_hora(df):
    """
    Gera gráfico consolidado de chamados por hora do dia.
    """
    df['Hora'] = pd.to_datetime(df['Iniciado em'], errors='coerce').dt.hour
    chamados_por_hora = df['Hora'].value_counts().sort_index()
    caminho = os.path.join(GRAPHS_DIR, 'chamados_por_hora.png')
    gerar_grafico(
        dados=chamados_por_hora,
        titulo='Chamados por Hora do Dia',
        xlabel='Hora do Dia',
        ylabel='Quantidade de Chamados',
        caminho_arquivo=caminho,
        horizontal=False,
        palette='Blues'
    )