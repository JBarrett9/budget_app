from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_googlecharts import GoogleCharts
from budgetapp.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
charts = GoogleCharts()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    charts.init_app(app)

    from budgetapp.users.routes import users
    from budgetapp.bills.routes import bills
    from budgetapp.main.routes import main
    from budgetapp.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(bills)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
