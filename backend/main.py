from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="/")
CORS(app)  # Permite conexión desde frontend (JS)

# Ejemplo de endpoint de prueba
@app.route("/api/saludo")
def saludo():
    return jsonify({"mensaje": "Hola desde Flask"})


# Servir archivos estáticos del frontend (index.html, etc.)
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# Para producción, cualquier ruta desconocida va al frontend
@app.errorhandler(404)
def fallback(e):
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True)
