# ============================================================
# config.py - Configuración central de la aplicación
# ============================================================
# Aquí centralizamos toda la configuración: 
# cadena de conexión a SQL Server y ajustes de Flask.
# Si cambias de servidor o base de datos, solo editas este archivo.
# ============================================================

import pyodbc

# ── Configuración de Flask ───────────────────────────────────
class Config:
    # Clave secreta usada por Flask para firmar cookies de sesión
    # Cámbiala por una cadena larga y aleatoria en producción
    SECRET_KEY = "inventario_umg_2026"

    # Modo debug: True muestra errores detallados en el navegador
    # Cámbialo a False antes de subir a producción
    DEBUG = True


# ── Configuración de la base de datos ───────────────────────
# Driver ODBC instalado con SQL Server Developer Edition.
# Verifica el nombre exacto en: Panel de Control → ODBC Data Sources
DB_DRIVER   = "ODBC Driver 17 for SQL Server"
DB_SERVER   = "localhost"          # Nombre del servidor o IP
DB_DATABASE = "inventario_db"      # Nombre de la BD que creaste con el script SQL
DB_TRUSTED  = "yes"                # "yes" = Windows Authentication (sin usuario/contraseña)


def get_connection():
    """
    Crea y retorna una conexión activa a SQL Server.
    Se llama cada vez que un modelo necesita hacer una consulta.
    Usa Windows Authentication, así no necesitas poner usuario/contraseña.
    """
    connection_string = (
        f"DRIVER={{{DB_DRIVER}}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        f"Trusted_Connection={DB_TRUSTED};"
    )
    return pyodbc.connect(connection_string)
