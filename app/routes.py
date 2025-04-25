from flask import render_template, jsonify, request
from datetime import datetime
import os
import pandas as pd
from app.config import DATA_DIR, GRAPHS_DIR
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

def init_routes(app):
    def obter_meses_disponiveis():
        """
        Retorna os meses disponíveis com base nos arquivos no diretório dados_tiflux,
        ordenados na sequência correta (janeiro, fevereiro, etc.).
        """
        mapeamento_meses = {
            'janeiro.xlsx': 'Janeiro',
            'fevereiro.xlsx': 'Fevereiro',
            'março.xlsx': 'Março',
            'abril.xlsx': 'Abril'
        }

        # Lista para manter a ordem correta dos meses
        ordem_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril']

        # Verifica os arquivos no diretório e mapeia para os meses disponíveis
        meses = []
        for arquivo in os.listdir(DATA_DIR):
            if arquivo in mapeamento_meses:
                meses.append(mapeamento_meses[arquivo])

        # Ordena os meses de acordo com a ordem definida
        meses_ordenados = [mes for mes in ordem_meses if mes in meses]
        return meses_ordenados

    @app.route('/')
    def dashboard():
        graficos = {
            'catalogo': [],
            'horas': [],
            'dias': [],
            'clientes': [],
            'meses': [],
            'total_por_mes': []  # Novo tipo de gráfico
        }

        if not os.path.exists(GRAPHS_DIR):
            os.makedirs(GRAPHS_DIR)

        # Lista todos os gráficos gerados
        for arquivo in os.listdir(GRAPHS_DIR):
            if arquivo.endswith('.png'):
                if 'itens_catalogo' in arquivo:
                    graficos['catalogo'].append(arquivo)
                elif 'por_hora' in arquivo:
                    graficos['horas'].append(arquivo)
                elif 'por_dia' in arquivo:
                    graficos['dias'].append(arquivo)
                elif 'clientes' in arquivo:
                    graficos['clientes'].append(arquivo)
                elif 'por_mes' in arquivo:
                    graficos['meses'].append(arquivo)
                elif 'total_por_mes' in arquivo:  # Novo gráfico
                    graficos['total_por_mes'].append(arquivo)

        return render_template(
            'dashboard.html',
            graficos=graficos,
            atualizado=datetime.now(),
            meses=obter_meses_disponiveis()
        )

    @app.route('/atualizar', methods=['POST'])
    def atualizar():
        """Atualiza todos os gráficos"""
        try:
            df_total = consolidar_dados_mensais(DATA_DIR)
            df_total['Mes'] = df_total['Iniciado em'].dt.strftime('%B').str.capitalize()

            # Gera todos os gráficos
            gerar_grafico_item_catalogo_anual(df_total)
            gerar_grafico_chamados_por_hora(df_total)
            gerar_grafico_chamados_por_dia(df_total)
            gerar_grafico_clientes_frequentes(df_total)
            gerar_grafico_chamados_por_mes(df_total)
            gerar_todos_os_graficos_chamados_por_hora(df_total)
            gerar_grafico_total_por_mes(df_total)  # Novo gráfico

            return jsonify({
                "status": "success",
                "message": "Relatórios atualizados!",
                "meses": obter_meses_disponiveis()
            })
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route('/clientes/<mes>', methods=['GET'])
    def listar_clientes_por_mes(mes):
        """
        Retorna os clientes mais frequentes para um mês específico ou total.
        """
        try:
            df_total = consolidar_dados_mensais(DATA_DIR)
            df_total['Mes'] = df_total['Iniciado em'].dt.strftime('%B').str.capitalize()

            if mes.lower() == 'total':
                df_filtrado = df_total
            else:
                df_filtrado = df_total[df_total['Mes'] == mes.capitalize()]

            clientes = df_filtrado['Cliente'].value_counts().head(15).to_dict()
            return jsonify({
                "status": "success",
                "clientes": clientes,
                "mes": mes.capitalize()
            })
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route('/dias/<mes>', methods=['GET'])
    def listar_chamados_por_dia_mes(mes):
        """
        Retorna os chamados por dia da semana para um mês específico ou total.
        """
        try:
            df_total = consolidar_dados_mensais(DATA_DIR)
            df_total['Mes'] = df_total['Iniciado em'].dt.strftime('%B').str.capitalize()

            if mes.lower() == 'total':
                df_filtrado = df_total
            else:
                df_filtrado = df_total[df_total['Mes'] == mes.capitalize()]

            df_filtrado['Dia_Semana'] = pd.to_datetime(df_filtrado['Iniciado em']).dt.day_name()
            dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            nomes_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
            chamados_por_dia = df_filtrado['Dia_Semana'].value_counts().reindex(dias_ordem, fill_value=0)
            chamados_por_dia_pt = {nomes_pt[i]: chamados_por_dia[dias_ordem[i]] for i in range(len(dias_ordem))}

            return jsonify({
                "status": "success",
                "dias": chamados_por_dia_pt,
                "mes": mes.capitalize()
            })
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500