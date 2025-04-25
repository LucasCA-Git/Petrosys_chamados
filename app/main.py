import os
import pandas as pd
from app.config import DATA_DIR

def consolidar_dados_mensais(diretorio_dados):
    """
    Consolida dados de todos os arquivos mensais garantindo que a coluna 'Mes' seja string.
    """
    arquivos = [f for f in os.listdir(diretorio_dados) 
               if f.endswith('.xlsx') and not f.startswith('dados_anuais')]
    
    dfs = []
    
    for arquivo in arquivos:
        caminho_arquivo = os.path.join(diretorio_dados, arquivo)
        try:
            df_mes = pd.read_excel(caminho_arquivo, engine='openpyxl')
            
            # Garante que o nome do mês seja string e capitalize (ex: "Janeiro")
            nome_mes = str(arquivo.replace('.xlsx', '')).capitalize()
            df_mes['Mes'] = nome_mes  # Adiciona como string
            
            dfs.append(df_mes)
            
        except Exception as e:
            print(f"⚠️ Erro ao processar {arquivo}: {str(e)}")
            continue
    
    if dfs:
        df_total = pd.concat(dfs, ignore_index=True)
        
        # Garante conversão para string e tratamento de valores nulos
        df_total['Mes'] = df_total['Mes'].astype(str).str.capitalize()
        
        # Conversão segura de datas
        if 'Iniciado em' in df_total.columns:
            df_total['Iniciado em'] = pd.to_datetime(df_total['Iniciado em'], errors='coerce')
            # Remove linhas com datas inválidas
            df_total = df_total.dropna(subset=['Iniciado em'])
        
        print(f"✅ Dados consolidados: {len(df_total)} registros de {len(dfs)} meses")
        return df_total
    else:
        raise ValueError("Nenhum dado válido encontrado")

def processar_dados():
    """Função principal com tratamento de erros reforçado"""
    from app.relatorios import gerar_relatorios_consolidados
    
    try:
        print("\n" + "="*50)
        print("Processando dados...")
        
        df_total = consolidar_dados_mensais(DATA_DIR)
        
        # Verificação final da coluna 'Mes'
        if 'Mes' not in df_total.columns:
            raise ValueError("Coluna 'Mes' não encontrada no DataFrame")
        
        print("Dados processados. Gerando relatórios...")
        gerar_relatorios_consolidados()
        
        print("✅ Processo concluído!")
        print("="*50 + "\n")
        return True
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        return False