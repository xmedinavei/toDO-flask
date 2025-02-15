from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from .config import Config
from .auth import auth
from .models import UserModel


login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# Para cuadno flask_login quiera cargar un usuario
@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)


def create_app():
    app = Flask(__name__) # Cargar la app en la clase Flask
    bootstrap = Bootstrap(app) # Inicialziar bootstrap

    app.config.from_object(Config)

    login_manager.init_app(app)

    app.register_blueprint(auth)

    return app
