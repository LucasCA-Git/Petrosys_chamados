from flask import Flask, render_template
from datetime import datetime
import os
from config import GRAPHS_DIR
from main import gerar_relatorios_consolidados

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Lista todos os gráficos disponíveis
    graficos = [f for f in os.listdir(GRAPHS_DIR) if f.endswith('.png')]
    
    # Agrupa por tipo para organização no template
    graficos_organizados = {
        'catalogo': [g for g in graficos if 'itens_catalogo' in g],
        'horas': [g for g in graficos if 'por_hora' in g],
        'dias': [g for g in graficos if 'por_dia' in g],
        'clientes': [g for g in graficos if 'clientes' in g]
    }
    
    return render_template(
        'dashboard.html',
        graficos=graficos_organizados,
        atualizado=datetime.now()
    )

@app.route('/atualizar', methods=['POST'])
def atualizar_dados():
    try:
        gerar_relatorios_consolidados()
        return "Dados atualizados com sucesso!", 200
    except Exception as e:
        return f"Erro ao atualizar: {str(e)}", 500