import os
import pandas as pd
from pandas.api.types import CategoricalDtype
import matplotlib.pyplot as plt
import seaborn as sns

# Função para ler arquivos XLSX
def ler_arquivos_xlsx(diretorio):
    """Lê todos os arquivos XLSX de um diretório e retorna um DataFrame consolidado."""
    arquivos = [f for f in os.listdir(diretorio) if f.endswith('.xlsx')]
    dfs = []
    
    for arquivo in arquivos:
        try:
            # Lê o arquivo Excel
            df = pd.read_excel(os.path.join(diretorio, arquivo))
            # Extrai o mês do nome do arquivo (removendo a extensão)
            mes = os.path.splitext(arquivo)[0]
            # Adiciona uma coluna com o mês de referência
            df['Mês_Referência'] = mes.capitalize()
            dfs.append(df)
        except Exception as e:
            print(f"Erro ao ler o arquivo {arquivo}: {str(e)}")
    
    if not dfs:
        raise ValueError("Nenhum arquivo XLSX válido encontrado no diretório.")
    
    return pd.concat(dfs, ignore_index=True)

# Função para gerar e salvar gráficos com base nos dados fornecidos
def gerar_grafico(dados, titulo, xlabel, ylabel, caminho_arquivo, tipo='bar', palette=None):
    """Gera e salva um gráfico (barra ou linha) com os dados fornecidos."""

    plt.figure(figsize=(10, 6))  # Define o tamanho do gráfico

    # Escolhe o tipo de gráfico
    if tipo == 'line':
        sns.lineplot(x=dados.index, y=dados.values, marker='o')
    elif tipo == 'bar':
        sns.barplot(x=dados.index, y=dados.values, palette=palette)
    else:
        raise ValueError("Tipo de gráfico inválido. Use 'line' ou 'bar'.")

    # Títulos e rótulos
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)

    # Adiciona valores diretamente no gráfico
    for i, v in enumerate(dados.values):
        plt.text(i, v + max(dados.values) * 0.01, str(v), ha='center', va='bottom', fontsize=11)

    # Organiza layout e salva imagem
    plt.tight_layout()
    plt.savefig(caminho_arquivo)
    plt.show()

# Função para gerar gráficos de análise temporal
def analise_temporal(df: pd.DataFrame, periodo: str):
    """Realiza análises temporais (dia da semana, hora e mês) e gera gráficos."""

    # Converte corretamente a coluna 'Iniciado em'
    df['Iniciado em'] = pd.to_datetime(df['Iniciado em'], errors='coerce')

    # Cria colunas auxiliares ANTES de tentar ordenar/categorizar
    df['Dia_Semana'] = df['Iniciado em'].dt.day_name()
    df['Hora'] = df['Iniciado em'].dt.hour
    df['Mes'] = df['Iniciado em'].dt.month

    # Ordena os dias da semana corretamente
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

    # Chamados por hora
    chamados_por_hora = df['Hora'].value_counts().sort_index()
    gerar_grafico(
        dados=chamados_por_hora,
        titulo=f'Chamados por hora do dia ({periodo})',
        xlabel='Hora do Dia',
        ylabel='Quantidade de Chamados',
        caminho_arquivo=f'graficos/chamados_por_hora_{periodo}.png',
        tipo='bar'
    )

    # Chamados por mês (agora usando o mês de referência)
    chamados_por_mes = df['Mês_Referência'].value_counts()
    gerar_grafico(
        dados=chamados_por_mes,
        titulo=f'Chamados por mês ({periodo})',
        xlabel='Mês',
        ylabel='Quantidade de Chamados',
        caminho_arquivo=f'graficos/chamados_por_mes_{periodo}.png',
        tipo='bar'
    )

# Função para exibir os clientes que mais abriram chamados
def solicitantes_mais_chamaram(df: pd.DataFrame, periodo: str):
    """Gera gráfico dos clientes que mais abriram chamados."""

    # Verifica se a coluna existe (alguns arquivos podem ter 'Cliente' ou 'Solicitante')
    coluna_clientes = 'Cliente' if 'Cliente' in df.columns else 'Solicitante'
    
    clientes = df[coluna_clientes].value_counts().sort_values(ascending=False)
    gerar_grafico(
        dados=clientes.head(10),  # Mostra apenas os 10 principais
        titulo=f'Clientes que mais chamaram ({periodo})',
        xlabel='Cliente',
        ylabel='Quantidade de Chamados',
        caminho_arquivo=f'graficos/clientes_mais_chamaram_{periodo}.png',
        tipo='bar'
    )

# Função para análise de avaliação dos chamados
def analise_avaliacao(df: pd.DataFrame, periodo: str):
    """Gera gráfico de distribuição das avaliações."""
    
    # Filtra apenas chamados com avaliação
    df_avaliacao = df[df['Avaliação'].notna()]
    
    if not df_avaliacao.empty:
        avaliacoes = df_avaliacao['Avaliação'].value_counts().sort_index()
        gerar_grafico(
            dados=avaliacoes,
            titulo=f'Distribuição das avaliações ({periodo})',
            xlabel='Avaliação',
            ylabel='Quantidade',
            caminho_arquivo=f'graficos/avaliacoes_{periodo}.png',
            tipo='bar',
            palette='viridis'
        )

# Função principal que consolida e gera todos os gráficos
def gerar_relatorios_consolidados(diretorio_dados):
    """Consolida dados de todos os arquivos e gera relatórios completos."""
    
    # Cria diretório para os gráficos se não existir
    os.makedirs('graficos', exist_ok=True)
    
    # Lê e consolida todos os dados
    df_total = ler_arquivos_xlsx(diretorio_dados)
    
    # Gera análises para o período total
    analise_temporal(df_total, "Período Total")
    solicitantes_mais_chamaram(df_total, "Período Total")
    analise_avaliacao(df_total, "Período Total")
    
    # Gera análises para cada mês individualmente
    meses = df_total['Mês_Referência'].unique()
    for mes in meses:
        df_mes = df_total[df_total['Mês_Referência'] == mes]
        analise_temporal(df_mes, mes)
        solicitantes_mais_chamaram(df_mes, mes)
        analise_avaliacao(df_mes, mes)
    
    return df_total

# Exemplo de uso
if __name__ == "__main__":
    # Diretório onde estão os arquivos XLSX
    diretorio_dados = './dados_tiflux'
    
    # Gera todos os relatórios
    dados_consolidados = gerar_relatorios_consolidados(diretorio_dados)
    
    # Opcional: salva os dados consolidados em um único arquivo
    dados_consolidados.to_excel('dados_consolidados.xlsx', index=False)