import os
from app.config import GRAPHS_DIR, DATA_DIR
from app.main import consolidar_dados_mensais
from app.graficos import (
    gerar_grafico_item_catalogo_anual,
    gerar_grafico_chamados_por_mes,
    gerar_grafico_chamados_por_dia,
    gerar_grafico_chamados_por_hora,
)

def gerar_relatorios_consolidados():
    """
    Consolida dados de todos os arquivos e gera relatórios completos.
    """
    os.makedirs(GRAPHS_DIR, exist_ok=True)
    print(f"Diretório de gráficos: {GRAPHS_DIR}")


    # Consolida os dados mensais
    df_total = consolidar_dados_mensais(DATA_DIR)
    print("Dados consolidados com sucesso.")


    # Salva o consolidado anual em um arquivo Excel
    caminho_arquivo_anual = os.path.join(DATA_DIR, 'dados_anuais.xlsx')
    df_total.to_excel(caminho_arquivo_anual, index=False)
    print(f"Arquivo consolidado salvo em: {caminho_arquivo_anual}")


    # Gera gráficos consolidados
    gerar_grafico_item_catalogo_anual(df_total)
    print("Gráfico de itens do catálogo gerado.")
    gerar_grafico_chamados_por_mes(df_total)
    print("Gráfico de chamados por mês gerado.")
    gerar_grafico_chamados_por_dia(df_total)
    print("Gráfico de chamados por dia gerado.")
    gerar_grafico_chamados_por_hora(df_total)
    print("Gráfico de chamados por hora gerado.")


    print("Relatórios gerados com sucesso!")