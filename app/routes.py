from flask import render_template, jsonify
from datetime import datetime
import os

def init_routes(app):
    @app.route('/')
    def dashboard():
        graficos = {
            'catalogo': [],
            'horas': [],
            'dias': [],
            'clientes': []
        }

        graphs_dir = app.config['GRAPHS_FOLDER']
        if not os.path.exists(graphs_dir):
            os.makedirs(graphs_dir)

        for f in os.listdir(graphs_dir):
            if f.endswith('.png'):
                if 'itens_catalogo' in f:
                    graficos['catalogo'].append(f)
                elif 'por_hora' in f:
                    graficos['horas'].append(f)
                elif 'por_dia' in f:
                    graficos['dias'].append(f)
                elif 'clientes' in f:
                    graficos['clientes'].append(f)

        return render_template('dashboard.html',
                               graficos=graficos,
                               atualizado=datetime.now())

    @app.route('/atualizar', methods=['POST'])
    def atualizar():
        try:
            # Importação local para evitar ciclos
            from app.relatorios import gerar_relatorios_consolidados
            gerar_relatorios_consolidados()
            return jsonify({"status": "success", "message": "Dados atualizados!"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500