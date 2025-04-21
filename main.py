from src.carregamento_dados import carregar_dados

if __name__ == "__main__":
    df = carregar_dados("dados_tiflux")
    print(df.head())
    print(f"Total de chamados: {len(df)}")
