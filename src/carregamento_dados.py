import pandas as pd
import os

def carregar_dados(caminho_pasta: str) -> pd.DataFrame:
    arquivos = [f for f in os.listdir(caminho_pasta) if f.endswith('.csv')]
    dfs = []

    for arquivo in arquivos:
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)
        df = pd.read_csv(
            caminho_arquivo,
            sep=';',
            encoding='utf-8',
            parse_dates=['Iniciado em', 'Assumido em', 'Atualizado em', 'Finalizado em'],
            date_parser=lambda x: pd.to_datetime(x, format='%d/%m/%Y %H:%M', errors='coerce')
        )
        dfs.append(df)

    df_geral = pd.concat(dfs, ignore_index=True)

    # Renomear colunas para remover espaços e facilitar o uso
    df_geral.columns = [col.strip().replace(' ', '_').replace('(', '').replace(')', '') for col in df_geral.columns]

    # Garantir que colunas de data sejam datetime (já vem tratado, mas por segurança)
    datas = ['Iniciado_em', 'Assumido_em', 'Atualizado_em', 'Finalizado_em']
    for col in datas:
        df_geral[col] = pd.to_datetime(df_geral[col], errors='coerce', dayfirst=True)

    # Criar coluna com dia da semana e hora
    df_geral['Dia_Semana'] = df_geral['Iniciado_em'].dt.day_name()
    df_geral['Hora'] = df_geral['Iniciado_em'].dt.hour

    return df_geral
