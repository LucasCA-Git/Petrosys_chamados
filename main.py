import calendar
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Função genérica para gerar gráficos
def gerar_grafico(dados, titulo, xlabel, ylabel, caminho_arquivo, tipo='bar', horizontal=False, palette='Blues'):
    """
    Gera gráficos de barras ou linhas com opções de orientação horizontal.
    """
    plt.figure(figsize=(16, 8))  # Define o tamanho do gráfico
    
    if tipo == 'bar':  # Gráfico de barras
        if horizontal:  # Gráfico de barras horizontal
            ax = sns.barplot(y=dados.index, x=dados.values, palette=palette, orient='h')
            # Adiciona os valores nas barras
            for p in ax.patches:
                ax.text(p.get_width() + 0.5, p.get_y() + p.get_height() / 2, f'{int(p.get_width())}', va='center')
        else:  # Gráfico de barras vertical
            ax = sns.barplot(x=dados.index, y=dados.values, palette=palette)
            # Adiciona os valores nas barras
            for p in ax.patches:
                ax.text(p.get_x() + p.get_width() / 2, p.get_height() + 0.5, f'{int(p.get_height())}', ha='center')
    elif tipo == 'line':  # Gráfico de linhas
        sns.lineplot(x=dados.index, y=dados.values, marker='o', linewidth=2.5)
    else:
        raise ValueError("Tipo de gráfico inválido. Use 'bar' ou 'line'.")  # Validação do tipo de gráfico

    # Configurações gerais do gráfico
    plt.title(titulo, fontsize=14, pad=20)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(rotation=45 if not horizontal else 0, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')  # Salva o gráfico no caminho especificado
    plt.close()

# Função para gerar gráfico consolidado de itens do catálogo
def gerar_grafico_item_catalogo_anual(df):
    # Verifica se a coluna 'Item do Catálogo' existe
    if 'Item do Catálogo' in df.columns:
        # Seleciona os 15 itens mais frequentes
        itens_catalogo = df['Item do Catálogo'].value_counts().head(15)
        # Gera o gráfico
        gerar_grafico(
            dados=itens_catalogo,
            titulo='Top 15 Problemas mais recorrentes',
            xlabel='Quantidade',
            ylabel='Item do Catálogo',
            caminho_arquivo='graficos/itens_catalogo_total_anual.png',
            horizontal=True,  # Gráfico horizontal
            palette='Blues_r'  # Paleta de cores
        )

# Função para gerar gráfico de chamados por hora
def gerar_grafico_chamados_por_hora(df, mes=None):
    try:
        # Converte a coluna de data e extrai a hora
        df['Hora'] = pd.to_datetime(df['Iniciado em'], errors='coerce', dayfirst=True).dt.hour
        # Conta os chamados por hora e garante todas as horas (0-23)
        chamados_por_hora = df['Hora'].value_counts().sort_index()
        chamados_por_hora = chamados_por_hora.reindex(range(24), fill_value=0)
        # Gera o gráfico
        plt.figure(figsize=(16, 6))
        ax = sns.barplot(x=chamados_por_hora.index, y=chamados_por_hora.values, palette='Blues')
        # Adiciona os valores nas barras
        for p in ax.patches:
            if p.get_height() > 0:
                ax.text(p.get_x() + p.get_width()/2, p.get_height() + 0.5, f'{int(p.get_height())}', ha='center')
        # Configurações do gráfico
        titulo = 'Chamados por Hora do Dia' + (f' ({mes})' if mes else ' (Total Anual)')
        plt.title(titulo, fontsize=14)
        plt.xlabel('Hora do Dia', fontsize=12)
        plt.ylabel('Quantidade de Chamados', fontsize=12)
        plt.xticks(range(0, 24), fontsize=10)
        plt.xlim(-0.5, 23.5)  # Garante que todas as horas sejam mostradas
        # Salva o gráfico
        caminho = f'graficos/chamados_por_hora_{mes.lower() if mes else "total"}.png'
        plt.tight_layout()
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"Erro ao gerar gráfico de chamados por hora: {str(e)}")

# Função para gerar gráficos de chamados por hora para todos os meses
def gerar_todos_os_graficos_chamados_por_hora(df):
    # Converte a coluna de data e remove valores inválidos
    df['Iniciado em'] = pd.to_datetime(df['Iniciado em'], errors='coerce', dayfirst=True)
    df = df.dropna(subset=['Iniciado em'])
    # Extrai o nome do mês
    df['Mes_Nome'] = df['Iniciado em'].dt.month.apply(lambda x: calendar.month_name[x].capitalize())
    meses_unicos = df['Mes_Nome'].unique()
    # Gera gráficos para cada mês
    for mes in meses_unicos:
        gerar_grafico_chamados_por_hora(df, mes)

# Função para gerar gráfico de chamados por dia da semana
def gerar_grafico_chamados_por_dia(df, mes=None):
    try:
        # Converte a coluna de data e extrai o dia da semana
        df['Dia_Semana'] = pd.to_datetime(df['Iniciado em'], dayfirst=True).dt.day_name()
        # Define a ordem dos dias da semana
        dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        nomes_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        # Conta os chamados por dia da semana
        chamados_por_dia = df['Dia_Semana'].value_counts().reindex(dias_ordem, fill_value=0)
        # Gera o gráfico
        plt.figure(figsize=(12, 6))
        ax = sns.barplot(x=nomes_pt, y=chamados_por_dia.values, palette='Blues')
        # Adiciona os valores nas barras
        for p in ax.patches:
            ax.text(p.get_x() + p.get_width()/2, p.get_height()+0.5, f'{int(p.get_height())}', ha='center')
        # Configurações do gráfico
        titulo = 'Chamados por Dia da Semana' + (f' ({mes})' if mes else ' (Total Anual)')
        plt.title(titulo, fontsize=14)
        plt.xlabel('Dia da Semana', fontsize=12)
        plt.ylabel('Quantidade', fontsize=12)
        plt.xticks(fontsize=10)
        plt.tight_layout()
        # Salva o gráfico
        caminho = f'graficos/chamados_por_dia_{mes.lower()}.png' if mes else 'graficos/chamados_por_dia_total.png'
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"Erro ao gerar gráfico de dias: {str(e)}")

# Função para gerar gráfico de clientes frequentes
def gerar_grafico_clientes_frequentes(df, mes=None):
    # Verifica se a coluna 'Cliente' existe
    if 'Cliente' in df.columns:
        # Seleciona os 15 clientes mais frequentes
        clientes_top = df['Cliente'].value_counts().head(15)
        # Gera o gráfico
        gerar_grafico(
            dados=clientes_top,
            titulo='Clientes que Mais Chamaram' + (f' ({mes})' if mes else ' (Total Anual)'),
            xlabel='Quantidade de Chamados',
            ylabel='Cliente',
            caminho_arquivo=f'graficos/clientes_frequentes_{mes.lower()}.png' if mes else 'graficos/clientes_frequentes_total.png',
            horizontal=True,
            palette='viridis'
        )

# Função para gerar gráficos mensais
def gerar_graficos_mensais(df, mes):
    gerar_grafico_chamados_por_dia(df, mes)  # Gráfico de chamados por dia da semana
    gerar_grafico_clientes_frequentes(df, mes)  # Gráfico de clientes frequentes
    gerar_grafico_chamados_por_hora(df, mes)  # Gráfico de chamados por hora

# Função para consolidar os dados de todas as planilhas
def consolidar_dados_mensais(diretorio_dados):
    arquivos = [f for f in os.listdir(diretorio_dados) if f.endswith('.xlsx')]  # Lista todos os arquivos .xlsx
    df_total = pd.DataFrame()  # DataFrame vazio para consolidar os dados
    for arquivo in arquivos:
        try:
            caminho_arquivo = os.path.join(diretorio_dados, arquivo)  # Caminho completo do arquivo
            df_mes = pd.read_excel(caminho_arquivo)  # Lê o arquivo Excel
            mes = os.path.splitext(arquivo)[0]  # Extrai o nome do mês
            gerar_graficos_mensais(df_mes, mes)  # Gera gráficos para o mês
            df_total = pd.concat([df_total, df_mes], ignore_index=True)  # Concatena os dados no DataFrame total
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {str(e)}")
    return df_total

# Função principal para gerar relatórios consolidados
def gerar_relatorios_consolidados(diretorio_dados):
    os.makedirs('graficos', exist_ok=True)  # Cria o diretório para os gráficos, se não existir
    try:
        df_total = consolidar_dados_mensais(diretorio_dados)  # Consolida os dados mensais
        gerar_grafico_item_catalogo_anual(df_total)  # Gráfico de itens do catálogo
        gerar_grafico_chamados_por_dia(df_total)  # Gráfico de chamados por dia
        gerar_grafico_clientes_frequentes(df_total)  # Gráfico de clientes frequentes
        gerar_grafico_chamados_por_hora(df_total)  # Gráfico de chamados por hora
        # Salva o consolidado anual
        caminho_anual = os.path.join(diretorio_dados, 'dados_anuais.xlsx')
        df_total.to_excel(caminho_anual, index=False)
        print("Relatórios gerados com sucesso!")
    except Exception as e:
        print(f"Erro ao gerar relatórios: {str(e)}")

# Ponto de entrada do programa
if __name__ == "__main__":
    diretorio_dados = './dados_tiflux'  # Diretório onde estão os arquivos Excel
    gerar_relatorios_consolidados(diretorio_dados)  # Gera os relatórios consolidados