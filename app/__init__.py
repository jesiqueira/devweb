from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'rota.login'
login_manager.login_message = 'Faça login para acessar essa página.'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    # Rotas
    from app.rotas import rota
    from app.controllers.usuarios.rotas import users
    from app.controllers.medicamento.rotas import medicine

    # Registrar Blueprint
    app.register_blueprint(rota)
    app.register_blueprint(users)
    app.register_blueprint(medicine)

    return manager
