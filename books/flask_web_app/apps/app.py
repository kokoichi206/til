from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import config


db = SQLAlchemy()

csrf = CSRFProtect()


def create_app(config_key):
    app = Flask(__name__)

    app.config.from_object(config[config_key])
    # app.config.from_mapping(
    #     SECRET_KEY="2AZffaeEI3P12H",
    #     SQLALCHEMY_DATABASE_URI="sqlite:////"
    #     + str(Path(__file__).parent.parent / 'local.sqlite'),
    #     SQLALCHEMY_TRACK_MODIFICATIONS=False,
    #     # SQLをコンソールログに出力
    #     SQLALCHEMY_ECHO=True,
    #     WTF_CSRF_SECRET_KEY="Acwu3U1p9xm8f",
    # )

    csrf.init_app(app)

    # SQLAlchemy と連携
    db.init_app(app)
    # Migrate とアプリを連携
    Migrate(app, db)

    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app
