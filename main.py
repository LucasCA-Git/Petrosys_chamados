import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def gerar_grafico(dados, titulo, xlabel, ylabel, caminho_arquivo, tipo='bar', horizontal=False, palette='Blues'):
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
    if 'Item do Catálogo' in df.columns:
        itens_catalogo = df['Item do Catálogo'].value_counts().head(15)  # Mostrar 30 itens
        gerar_grafico(
            dados=itens_catalogo,
            titulo='Top 30 Itens Mais Frequentes do Catálogo',
            xlabel='Quantidade',
            ylabel='Item do Catálogo',
            caminho_arquivo='graficos/itens_catalogo_total_anual.png',
            horizontal=True,
            palette='Blues_r'
        )
def gerar_grafico_chamados_por_hora(df, mes=None):
    try:
        # Converter a coluna de data e extrair a hora
        df['Hora'] = pd.to_datetime(df['Iniciado em'], errors='coerce', dayfirst=True).dt.hour
        
        # Contar chamados por hora e garantir todas as horas (0-23)
        chamados_por_hora = df['Hora'].value_counts().sort_index()
        chamados_por_hora = chamados_por_hora.reindex(range(24), fill_value=0)
        
        # Configurar o gráfico
        plt.figure(figsize=(16, 6))
        ax = sns.barplot(x=chamados_por_hora.index, 
                        y=chamados_por_hora.values, 
                        palette='Blues')
        
        # Adicionar valores nas barras
        for p in ax.patches:
            if p.get_height() > 0:  # Só mostra valor se houver chamados
                ax.text(p.get_x() + p.get_width()/2, 
                       p.get_height() + 0.5, 
                       f'{int(p.get_height())}', 
                       ha='center')
        
        # Configurações do gráfico
        titulo = 'Chamados por Hora do Dia' + (f' ({mes})' if mes else ' (Total Anual)')
        plt.title(titulo, fontsize=14)
        plt.xlabel('Hora do Dia', fontsize=12)
        plt.ylabel('Quantidade de Chamados', fontsize=12)
        plt.xticks(range(0, 24), fontsize=10)
        plt.xlim(-0.5, 23.5)  # Garante que todas as horas sejam mostradas
        
        # Salvar o gráfico
        caminho = f'graficos/chamados_por_hora_{mes.lower() if mes else "total"}.png'
        plt.tight_layout()
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close()
        
    except Exception as e:
        print(f"Erro ao gerar gráfico de chamados por hora: {str(e)}")


def gerar_todos_os_graficos_chamados_por_hora(df):
    df['Iniciado em'] = pd.to_datetime(df['Iniciado em'], errors='coerce', dayfirst=True)
    df = df.dropna(subset=['Iniciado em'])  # Garante que datas inválidas sejam removidas

    # Gera gráficos mensais automaticamente
    df['Mes_Nome'] = df['Iniciado em'].dt.month.apply(lambda x: calendar.month_name[x].capitalize())
    meses_unicos = df['Mes_Nome'].unique()

    for mes in meses_unicos:
        gerar_grafico_chamados_por_hora(df, mes)

def gerar_grafico_chamados_por_dia(df, mes=None):
    try:
        # Converter datas com formato dia/mês/ano
        df['Dia_Semana'] = pd.to_datetime(df['Iniciado em'], dayfirst=True).dt.day_name()
        
        dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        nomes_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        
        chamados_por_dia = df['Dia_Semana'].value_counts().reindex(dias_ordem, fill_value=0)
        
        plt.figure(figsize=(12, 6))
        ax = sns.barplot(x=nomes_pt, y=chamados_por_dia.values, palette='Blues')
        
        for p in ax.patches:
            ax.text(p.get_x() + p.get_width()/2, p.get_height()+0.5, 
                   f'{int(p.get_height())}', ha='center')
        
        titulo = 'Chamados por Dia da Semana' + (f' ({mes})' if mes else ' (Total Anual)')
        plt.title(titulo, fontsize=14)
        plt.xlabel('Dia da Semana', fontsize=12)
        plt.ylabel('Quantidade', fontsize=12)
        plt.xticks(fontsize=10)
        plt.tight_layout()
        
        caminho = f'graficos/chamados_por_dia_{mes.lower()}.png' if mes else 'graficos/chamados_por_dia_total.png'
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"Erro ao gerar gráfico de dias: {str(e)}")

def gerar_grafico_clientes_frequentes(df, mes=None):
    if 'Cliente' in df.columns:
        clientes_top = df['Cliente'].value_counts().head(15)  # Mostrar top 15 clientes
        gerar_grafico(
            dados=clientes_top,
            titulo='Clientes que Mais Chamaram' + (f' ({mes})' if mes else ' (Total Anual)'),
            xlabel='Quantidade de Chamados',
            ylabel='Cliente',
            caminho_arquivo=f'graficos/clientes_frequentes_{mes.lower()}.png' if mes else 'graficos/clientes_frequentes_total.png',
            horizontal=True,
            palette='viridis'
        )

#graficos mensais
def gerar_graficos_mensais(df, mes):
    gerar_grafico_chamados_por_dia(df, mes)
    gerar_grafico_clientes_frequentes(df, mes)
    gerar_grafico_chamados_por_hora(df, mes)
  

def consolidar_dados_mensais(diretorio_dados):
    arquivos = [f for f in os.listdir(diretorio_dados) if f.endswith('.xlsx')]
    df_total = pd.DataFrame()

    for arquivo in arquivos:
        try:
            caminho_arquivo = os.path.join(diretorio_dados, arquivo)
            df_mes = pd.read_excel(caminho_arquivo)
            mes = os.path.splitext(arquivo)[0]
            gerar_graficos_mensais(df_mes, mes)
            df_total = pd.concat([df_total, df_mes], ignore_index=True)
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {str(e)}")

    return df_total
    

def gerar_relatorios_consolidados(diretorio_dados):
    os.makedirs('graficos', exist_ok=True)


    try:
        df_total = consolidar_dados_mensais(diretorio_dados)
        
        # Gráficos anuais
        gerar_grafico_item_catalogo_anual(df_total)
        gerar_grafico_chamados_por_dia(df_total)
        gerar_grafico_clientes_frequentes(df_total)
        gerar_grafico_chamados_por_hora(df_total)

        # Salvar consolidado
        caminho_anual = os.path.join(diretorio_dados, 'dados_anuais.xlsx')
        df_total.to_excel(caminho_anual, index=False)
        
        print("Relatórios gerados com sucesso!")
    except Exception as e:
        print(f"Erro ao gerar relatórios: {str(e)}")

if __name__ == "__main__":
    diretorio_dados = './dados_tiflux'
    gerar_relatorios_consolidados(diretorio_dados)