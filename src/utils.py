import pandas as pd

def tratar_datas(df):
    """Converte as colunas de data para o formato datetime"""
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    return df
