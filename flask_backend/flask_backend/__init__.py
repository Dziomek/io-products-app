from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .database_connector import DatabaseConnector

app = Flask(__name__)
CORS(app)
jwt = JWTManager(app)
app.config.from_prefixed_env()
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
db = DatabaseConnector

if __name__ == '__main__':
    app.run()

from . import views
from . import auth