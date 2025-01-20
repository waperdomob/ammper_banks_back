import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
# Importa las extensiones
from extensions import db, jwt

# Importa blueprints
from routes.auth import auth_bp
from routes.banks import banks_bp

load_dotenv()
# Configuración de la app
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD')

app = Flask(__name__)

db_uri = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa extensiones
db.init_app(app)
jwt.init_app(app)
CORS(app)

# Registra blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(banks_bp, url_prefix='/api/banks')


if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)
