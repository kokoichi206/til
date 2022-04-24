from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import config


db = SQLAlchemy()

csrf = CSRFProtect()

login_manager = LoginManager()
# 未ログイン時にリダイレクトするエンドポイント
login_manager.login_view = "auth.signup"
# login_message属性にログイン後に表示するメッセージ
login_manager.login_mesasge = ""


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

    login_manager.init_app(app)

    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    from apps.auth import views as auth_views

    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    from apps.detector import views as dt_views

    # アプリケーションルートにするため、prefix は指定しない。
    app.register_blueprint(dt_views.dt)

    return app
