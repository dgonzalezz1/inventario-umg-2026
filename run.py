# ============================================================
# run.py - Punto de entrada de la aplicación
# ============================================================
# Este es el archivo que ejecutas para iniciar el servidor.
# Comando: python run.py
# Luego abre el navegador en: http://localhost:5000
# ============================================================

import sys
import os

# Agregamos la carpeta raíz al path para que Python encuentre los módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

# Creamos la instancia de la aplicación usando la fábrica
app = create_app()

if __name__ == "__main__":
    print("=" * 50)
    print("  Sistema de Gestión de Inventarios")
    print("  Universidad Mariano Gálvez - 2026")
    print("=" * 50)
    print("  Servidor corriendo en: http://localhost:5000")
    print("  Presiona Ctrl+C para detener el servidor")
    print("=" * 50)

    # debug=True: recarga automáticamente al guardar cambios
    # use_reloader=False: evita que cargar_estructuras() corra dos veces
    app.run(debug=True, use_reloader=False)
