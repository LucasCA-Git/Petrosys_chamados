import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def gerar_grafico(dados, titulo, xlabel, ylabel, caminho_arquivo, tipo='bar', horizontal=False, palette='Set2'):
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
    plt.xticks(rotation=45 if not horizontal else 0, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
    plt.close()

def gerar_grafico_item_catalogo_anual(df):
    """
    Gera gráfico horizontal consolidado para os itens do catálogo (dados anuais).
    """
    if 'Item do Catálogo' in df.columns:
        itens_catalogo = df['Item do Catálogo'].value_counts().head(10)
        gerar_grafico(
            dados=itens_catalogo,
            titulo='Itens do Catálogo Mais Frequentes (Total Anual)',
            xlabel='Quantidade',
            ylabel='Item do Catálogo',
            caminho_arquivo='graficos/itens_catalogo_total_anual.png',
            horizontal=True
        )
    else:
        print("Coluna 'Item do Catálogo' não encontrada no DataFrame.")

def gerar_grafico_chamados_por_mes_anual(df):
    """
    Gera gráfico consolidado de chamados por mês (dados anuais).
    """
    df['Mes'] = pd.to_datetime(df['Iniciado em'], errors='coerce').dt.strftime('%B')
    chamados_por_mes = df['Mes'].value_counts().sort_index()
    gerar_grafico(
        dados=chamados_por_mes,
        titulo='Chamados por Mês (Total Anual)',
        xlabel='Mês',
        ylabel='Quantidade de Chamados',
        caminho_arquivo='graficos/chamados_por_mes_total_anual.png'
    )

def gerar_grafico_total_por_mes(df):
    """
    Gera gráfico consolidado de chamados totais por mês (janeiro, fevereiro, março, abril).
    """
    df['Mes'] = pd.to_datetime(df['Iniciado em'], errors='coerce').dt.strftime('%B')
    chamados_por_mes = df['Mes'].value_counts().reindex(
        ['January', 'February', 'March', 'April'], fill_value=0
    )
    gerar_grafico(
        dados=chamados_por_mes,
        titulo='Chamados Totais por Mês (Janeiro a Abril)',
        xlabel='Mês',
        ylabel='Quantidade de Chamados',
        caminho_arquivo='graficos/chamados_totais_por_mes.png'
    )

def gerar_graficos_mensais(df, mes):
    """
    Gera gráficos para os dados de um mês específico.
    """
    # Chamados por dia da semana
    df['Dia_Semana'] = pd.to_datetime(df['Iniciado em'], errors='coerce').dt.day_name()
    chamados_por_dia = df['Dia_Semana'].value_counts().sort_index()
    gerar_grafico(
        dados=chamados_por_dia,
        titulo=f'Chamados por Dia da Semana ({mes})',
        xlabel='Dia da Semana',
        ylabel='Quantidade de Chamados',
        caminho_arquivo=f'graficos/chamados_por_dia_{mes}.png'
    )

    # Chamados por hora
    df['Hora'] = pd.to_datetime(df['Iniciado em'], errors='coerce').dt.hour
    chamados_por_hora = df['Hora'].value_counts().sort_index()
    gerar_grafico(
        dados=chamados_por_hora,
        titulo=f'Chamados por Hora do Dia ({mes})',
        xlabel='Hora do Dia',
        ylabel='Quantidade de Chamados',
        caminho_arquivo=f'graficos/chamados_por_hora_{mes}.png'
    )

def consolidar_dados_mensais(diretorio_dados):
    """
    Consolida os dados de todos os arquivos mensais em um único DataFrame.
    """
    arquivos = [f for f in os.listdir(diretorio_dados) if f.endswith('.xlsx')]
    df_total = pd.DataFrame()

    for arquivo in arquivos:
        caminho_arquivo = os.path.join(diretorio_dados, arquivo)
        df_mes = pd.read_excel(caminho_arquivo)
        mes = os.path.splitext(arquivo)[0]  # Nome do mês a partir do arquivo
        gerar_graficos_mensais(df_mes, mes)  # Gera gráficos para o mês
        df_total = pd.concat([df_total, df_mes], ignore_index=True)

    return df_total

def gerar_relatorios_consolidados(diretorio_dados):
    """
    Consolida dados de todos os arquivos e gera relatórios completos.
    """
    # Cria diretório para os gráficos
    os.makedirs('graficos', exist_ok=True)

    # Consolida os dados mensais
    df_total = consolidar_dados_mensais(diretorio_dados)

    # Salva o consolidado anual
    caminho_arquivo_anual = os.path.join(diretorio_dados, 'dados_anuais.xlsx')
    df_total.to_excel(caminho_arquivo_anual, index=False)

    # Gera gráficos consolidados
    gerar_grafico_item_catalogo_anual(df_total)
    gerar_grafico_chamados_por_mes_anual(df_total)
    gerar_grafico_total_por_mes(df_total)

    print("Relatórios gerados com sucesso!")

# Exemplo de uso
if __name__ == "__main__":
    # Diretório onde estão os arquivos mensais
    diretorio_dados = './dados_tiflux'

    # Gera relatórios consolidados
    gerar_relatorios_consolidados(diretorio_dados)