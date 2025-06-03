from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import sqlite3

# --- Configuración de base de datos SQLite manual ---
class ProyectoDB:
    def __init__(self, db_name="proyecto.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS rol (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_rol TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            rol_id INTEGER,
            FOREIGN KEY (rol_id) REFERENCES rol(id)
        );
        """)
        self.conn.commit()

# Inicializa base de datos
db = ProyectoDB()

# --- Configurar la app de Flask ---
app = Flask(__name__, static_folder="../frontend", static_url_path="/")
CORS(app)  # Permite solicitudes desde el frontend

# Ruta API de prueba
@app.route("/api/saludo")
def saludo():
    return jsonify({"mensaje": "Hola desde Flask con backend unificado"})

# Servir frontend (index.html u otro)
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# Fallback para SPA (React/Vue/etc.)
@app.errorhandler(404)
def fallback(e):
    return send_from_directory(app.static_folder, "index.html")

# --- Ejecutar servidor ---
if __name__ == "__main__":
    app.run(debug=True)
