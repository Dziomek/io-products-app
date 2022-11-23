from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .models import db

app = Flask(__name__)
CORS(app)
jwt = JWTManager(app)
app.config.from_prefixed_env()
db.init_app(app)

##with app.app_context():
    ##db.create_all()

if __name__ == '__main__':
    app.run()

from . import views