import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from app.config import GRAPHS_DIR

def gerar_grafico(dados, titulo, xlabel, ylabel, caminho_arquivo, tipo='bar', horizontal=False, palette='Blues'):
    """Função base para geração de gráficos"""
    plt.figure(figsize=(16, 8))
    
    if tipo == 'bar':
        if horizontal:
            ax = sns.barplot(y=dados.index, x=dados.values, palette=palette, orient='h')
            for p in ax.patches:
                ax.text(p.get_width() + 0.5, p.get_y() + p.get_height()/2, f'{int(p.get_width())}', va='center')
        else:
            ax = sns.barplot(x=dados.index, y=dados.values, palette=palette)
            for p in ax.patches:
                ax.text(p.get_x() + p.get_width()/2, p.get_height() + 0.5, f'{int(p.get_height())}', ha='center')
    elif tipo == 'line':
        sns.lineplot(x=dados.index, y=dados.values, marker='o', linewidth=2.5)
    
    plt.title(titulo, fontsize=14, pad=20)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.tight_layout()
    plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
    plt.close()

def gerar_grafico_item_catalogo_anual(df):
    """Gera gráfico de itens do catálogo para cada mês e total"""
    if 'Item do Catálogo' not in df.columns:
        return

    # Gráfico TOTAL
    itens_total = df['Item do Catálogo'].value_counts().head(15)
    caminho_total = os.path.join(GRAPHS_DIR, 'itens_catalogo_total.png')
    gerar_grafico(itens_total, 'Top 15 Itens do Catálogo (Total)', 
                 'Quantidade', 'Item do Catálogo', caminho_total, 
                 horizontal=True, palette='Blues_r')

    # Gráficos por MÊS
    for mes in df['Mes'].unique():
        df_mes = df[df['Mes'] == mes]
        itens_mes = df_mes['Item do Catálogo'].value_counts().head(10)
        caminho_mes = os.path.join(GRAPHS_DIR, f'itens_catalogo_{mes.lower()}.png')
        gerar_grafico(itens_mes, f'Top 10 Itens do Catálogo - {mes}', 
                     'Quantidade', 'Item do Catálogo', caminho_mes, 
                     horizontal=True, palette='Blues_r')

def gerar_grafico_chamados_por_hora(df, mes=None):
    """Gera gráfico de chamados por hora do dia"""
    df['Hora'] = pd.to_datetime(df['Iniciado em']).dt.hour
    
    if mes:
        df = df[df['Mes'] == mes.capitalize()]
    
    chamados_por_hora = df['Hora'].value_counts().sort_index().reindex(range(24), fill_value=0)
    nome_arquivo = f'chamados_por_hora_{mes.lower()}.png' if mes else 'chamados_por_hora_total.png'
    
    gerar_grafico(chamados_por_hora, 
                 f'Chamados por Hora ({mes if mes else "Total"})',
                 'Hora do Dia', 
                 'Quantidade de Chamados', 
                 os.path.join(GRAPHS_DIR, nome_arquivo),
                 tipo='line')

def gerar_grafico_total_por_mes(df):
    """Gera gráfico de barras com o total de chamados por mês (NOVO)"""
    total_por_mes = df['Mes'].value_counts().sort_index()
    
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x=total_por_mes.index, y=total_por_mes.values, palette="viridis")
    
    # Adiciona os valores em cima de cada barra
    for p in ax.patches:
        ax.annotate(f"{int(p.get_height())}", 
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha='center', va='center', xytext=(0, 10), 
                   textcoords='offset points')
    
    plt.title("Total de Chamados por Mês", fontsize=14)
    plt.xlabel("Mês")
    plt.ylabel("Quantidade de Chamados")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    caminho = os.path.join(GRAPHS_DIR, "total_por_mes.png")
    plt.savefig(caminho, dpi=300, bbox_inches='tight')
    plt.close()

def gerar_grafico_chamados_por_dia(df, mes=None):
    """Gera gráfico de chamados por dia da semana"""
    if mes:
        df = df[df['Mes'] == mes.capitalize()]
    
    # Mapeia dias da semana para português
    dias_pt = {
        'Monday': 'Segunda',
        'Tuesday': 'Terça',
        'Wednesday': 'Quarta',
        'Thursday': 'Quinta',
        'Friday': 'Sexta',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    
    df['Dia_Semana'] = pd.to_datetime(df['Iniciado em']).dt.day_name().map(dias_pt)
    chamados_por_dia = df['Dia_Semana'].value_counts().reindex(list(dias_pt.values()), fill_value=0)
    
    caminho = os.path.join(GRAPHS_DIR, 
                         f'chamados_por_dia_{mes.lower()}.png' if mes 
                         else 'chamados_por_dia_total.png')
    
    titulo = f'Chamados por Dia ({mes if mes else "Total"})'
    
    gerar_grafico(chamados_por_dia, titulo, 'Dia da Semana', 
                 'Quantidade de Chamados', caminho, palette='viridis')

def gerar_grafico_clientes_frequentes(df, mes=None):
    """Gera gráfico de clientes mais frequentes"""
    if 'Cliente' not in df.columns:
        return

    if mes:
        df = df[df['Mes'] == mes.capitalize()]
    
    clientes_top = df['Cliente'].value_counts().head(15)
    caminho = os.path.join(GRAPHS_DIR, 
                         f'clientes_frequentes_{mes.lower()}.png' if mes 
                         else 'clientes_frequentes_total.png')
    
    titulo = f'Top 15 Clientes  ({mes if mes else "Total"})'
    
    gerar_grafico(clientes_top, titulo, 'Quantidade de Chamados', 
                 'Cliente ', caminho, horizontal=True, palette='magma')

def gerar_todos_os_graficos_chamados_por_hora(df):
    """Gera gráficos de chamados por hora para todos os meses"""
    # Gráfico comparativo entre meses
    plt.figure(figsize=(16, 8))
    meses = df['Mes'].unique()
    
    for mes in meses:
        df_mes = df[df['Mes'] == mes]
        chamados = df_mes['Iniciado em'].dt.hour.value_counts().sort_index().reindex(range(24), fill_value=0)
        sns.lineplot(x=chamados.index, y=chamados.values, label=mes, linewidth=2.5)
    
    plt.title('Comparativo Mensal - Chamados por Hora', fontsize=14, pad=20)
    plt.xlabel('Hora do Dia', fontsize=12)
    plt.ylabel('Quantidade de Chamados', fontsize=12)
    plt.legend(title='Mês')
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPHS_DIR, 'comparativo_chamados_por_hora.png'), 
               dpi=300, bbox_inches='tight')
    plt.close()
    
    # Gráficos individuais por mês
    for mes in meses:
        gerar_grafico_chamados_por_hora(df, mes)

def gerar_grafico_chamados_por_mes(df):
    """Gera gráfico de evolução mensal de chamados"""
    chamados_por_mes = df['Mes'].value_counts().sort_index()
    
    plt.figure(figsize=(16, 8))
    sns.lineplot(x=chamados_por_mes.index, y=chamados_por_mes.values, 
                marker='o', linewidth=2.5, color='royalblue')
    plt.title('Evolução Mensal de Chamados', fontsize=14, pad=20)
    plt.xlabel('Mês', fontsize=12)
    plt.ylabel('Quantidade de Chamados', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPHS_DIR, 'evolucao_mensal_chamados.png'), 
               dpi=300, bbox_inches='tight')
    plt.close()