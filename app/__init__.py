# ============================================================
# app/__init__.py - Fábrica de la aplicación Flask
# ============================================================
# Esta función crea y configura la aplicación Flask.
# Registra el Blueprint del controlador y carga las estructuras
# de datos con los datos de la BD al iniciar.
# ============================================================

from flask import Flask
from config import Config


def create_app():
    """
    Función de fábrica: crea la instancia de Flask,
    aplica la configuración y registra los blueprints.
    """
    # Creamos la aplicación Flask
    # __name__ le dice a Flask dónde está la carpeta raíz
    app = Flask(__name__, template_folder="views/templates")
    app.config.from_object(Config)

    # ── Registramos el Blueprint del controlador ─────────────
    # Importamos aquí para evitar importaciones circulares
    from app.controllers.inventario_controller import inventario_bp, cargar_estructuras
    app.register_blueprint(inventario_bp)

    # ── Cargamos estructuras de datos al iniciar ─────────────
    # Dentro del contexto de la app para poder usar la BD
    with app.app_context():
        cargar_estructuras()

    return app
