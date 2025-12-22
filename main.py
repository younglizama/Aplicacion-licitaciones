import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

# --- CONFIGURACIÓN DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'src'))

from src.views.main_window import MainWindow

if __name__ == "__main__":
    # 1. Crear la instancia de la aplicación
    app = QApplication(sys.argv)
    
    # 2. Configurar Estilo
    app.setStyle("Fusion")

    # 3. APLICAR TEMA OSCURO
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(15, 23, 42))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(30, 41, 59))
    palette.setColor(QPalette.AlternateBase, QColor(51, 65, 85))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(51, 65, 85))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(59, 130, 246))
    palette.setColor(QPalette.Highlight, QColor(59, 130, 246))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)

    # 4. Iniciar la Ventana Principal
    window = MainWindow()
    window.show()
    
    # --- BLOQUE NUEVO PARA CERRAR LA PANTALLA DE CARGA (SPLASH) ---
    try:
        import pyi_splash # type: ignore
        # Opcional: Actualizar mensaje si quieres
        # pyi_splash.update_text('¡Carga completa!') 
        pyi_splash.close()
    except ImportError:
        # Si no estamos ejecutando el .exe con splash, esto simplemente se ignora
        pass
    # --------------------------------------------------------------
    
    # 5. Ejecutar el bucle principal
    sys.exit(app.exec())