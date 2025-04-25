import os
from datetime import datetime
from app.config import GRAPHS_DIR, DATA_DIR
from app.main import consolidar_dados_mensais
from app.graficos import (
    gerar_grafico_item_catalogo_anual,
    gerar_grafico_chamados_por_hora,
    gerar_grafico_chamados_por_dia,
    gerar_grafico_clientes_frequentes,
    gerar_todos_os_graficos_chamados_por_hora,
    gerar_grafico_chamados_por_mes,
    gerar_grafico_total_por_mes
)

def gerar_relatorios_consolidados():
    """
    Gera todos os relatórios e gráficos automaticamente, incluindo:
    - Gráficos individuais por mês
    - Gráficos consolidados (total)
    - Gráficos comparativos
    """
    try:
        # 1. Configuração inicial
        os.makedirs(GRAPHS_DIR, exist_ok=True)
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Iniciando geração de relatórios...")

        # 2. Consolida dados de todos os arquivos
        df_total = consolidar_dados_mensais(DATA_DIR)
        
        # Adiciona coluna de mês padronizada (ex: "Janeiro")
        df_total['Mes'] = df_total['Iniciado em'].dt.strftime('%B').str.capitalize()
        
        total_registros = len(df_total)
        meses = df_total['Mes'].unique()
        print(f"✅ Dados consolidados: {total_registros} registros em {len(meses)} meses ({', '.join(meses)})")

        # 3. Geração de gráficos
        print("\n🔨 Gerando gráficos:")
        
        # Gráfico NOVO - Total por mês
        gerar_grafico_total_por_mes(df_total)
        print("  ✅ Total de chamados por mês")

        # Itens do catálogo
        gerar_grafico_item_catalogo_anual(df_total)
        print("  ✅ Itens do catálogo (por mês e total)")

        # Chamados por hora
        gerar_grafico_chamados_por_hora(df_total)  # Total
        gerar_todos_os_graficos_chamados_por_hora(df_total)  # Mensal + comparativo
        print("  ✅ Chamados por hora (individual e comparativo)")

        # Chamados por dia
        gerar_grafico_chamados_por_dia(df_total)
        print("  ✅ Chamados por dia da semana")

        # Clientes frequentes
        gerar_grafico_clientes_frequentes(df_total)
        print("  ✅ Clientes mais frequentes")

        # Evolução mensal
        gerar_grafico_chamados_por_mes(df_total)
        print("  ✅ Evolução mensal de chamados")

        # 4. Finalização
        print(f"\n✅ Relatórios gerados com sucesso em: {GRAPHS_DIR}")
        return True

    except Exception as e:
        print(f"\n❌ Erro ao gerar relatórios: {str(e)}")
        raise