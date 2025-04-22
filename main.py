from src.carregamento_dados import carregar_dados
from src.analise_geral import resumo_geral
from src.analise_tipo import tipos_de_chamado, chamados_sem_tipo
from src.analise_temporal import chamados_por_temporalidade
from src.previsao_chamados import previsao_volume_chamados

def main():
    caminho_pasta = 'dados_tiflux'  # Altere esse nome se sua pasta tiver outro nome
    df = carregar_dados(caminho_pasta)

    # Chamadas de análise geral
    resumo_geral(df)

    # Chamadas de análise por tipo de chamado
    tipos_de_chamado(df)
    chamados_sem_tipo(df)

    # Análise temporal
    chamados_por_temporalidade(df)

    # Previsão de volume de chamados
    previsao_volume_chamados(df)

if __name__ == "__main__":
    main()
