from flask import Flask

# Criação do objeto Flask
app = Flask(__name__)

# Configurações
from .config import GRAPHS_DIR
app.config['GRAPHS_FOLDER'] = GRAPHS_DIR

# Importar rotas DEPOIS de criar o app
from .routes import init_routes
init_routes(app)