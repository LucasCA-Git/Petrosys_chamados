from app.routes import app
from config import DATA_DIR, GRAPHS_DIR

if __name__ == '__main__':
    print(f"""
    ========================================
      Dashboard Tiflux - Painel de Análise
    ========================================
    • Dados em: {DATA_DIR}
    • Gráficos em: {GRAPHS_DIR}
    • Acesse: http://localhost:5000
    """)
    app.run(debug=True)