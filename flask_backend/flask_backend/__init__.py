from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .models import db
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .models import User

app = Flask(__name__)
CORS(app)
jwt = JWTManager(app)
app.config.from_prefixed_env()
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()

from . import views