# Archivo generado automáticamente
import os
import sys

def resource_path(relative_path):
    """ 
    Obtiene la ruta absoluta al recurso. 
    Funciona para desarrollo (dev) y para el ejecutable compilado (PyInstaller).
    """
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # En modo desarrollo, usa la ruta actual
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# --- RUTAS GLOBALES ---

# 1. Rutas de ASSETS (Van DENTRO del .exe: Iconos, Plantillas fijas)
# Usamos resource_path porque queremos que viajen con el programa
ASSETS_DIR = resource_path("assets")
TEMPLATE_DIR = os.path.join(ASSETS_DIR, "templates")
ICONS_DIR = os.path.join(ASSETS_DIR, "icons")
DOCS_BASE_DIR = os.path.join(ASSETS_DIR, "docs_base")

# 2. Rutas de DATOS DE USUARIO (Van FUERA del .exe)
# La base de datos y los outputs deben guardarse en la carpeta donde está el .exe, 
# no adentro, porque si no se borrarían al cerrar el programa.
BASE_DIR = os.getcwd() # Ruta donde el usuario tiene el archivo .exe o .py
DB_PATH = os.path.join(BASE_DIR, "licitaciones.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Asegurar que la carpeta output exista
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)