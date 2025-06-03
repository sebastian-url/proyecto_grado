from flask import Flask, send_from_directory
from config import db, DATABASE_URL
import os

def create_app():
    app = Flask(__name__, static_folder="../frontend", static_url_path="")

    # Configuración de la base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Ruta para servir HTML del frontend
    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "login.html")

    @app.route("/<path:filename>")
    def frontend_files(filename):
        return send_from_directory(app.static_folder, filename)

    return app
