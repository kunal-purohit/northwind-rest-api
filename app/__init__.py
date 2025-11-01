from flask import Flask
from .config import config_by_name
from .database import init_app
from .routes import customer_bp, order_bp, product_bp


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config_by_name[config_name])

    init_app(app)

    app_root = "/api"

    app.register_blueprint(customer_bp, url_prefix=app_root)
    app.register_blueprint(product_bp, url_prefix=app_root)
    app.register_blueprint(order_bp, url_prefix=app_root)

    @app.route("/")
    def index():
        return "<h1>Northwind REST API using Flask.</h1>"

    return app
