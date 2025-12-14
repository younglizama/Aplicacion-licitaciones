import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

# --- CONFIGURACIÓN DE RUTAS ---
# Esto asegura que Python encuentre la carpeta 'src' sin importar desde dónde ejecutes
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'src'))

# Importamos la ventana principal que definimos en los pasos anteriores
from src.views.main_window import MainWindow

if __name__ == "__main__":
    # 1. Crear la instancia de la aplicación
    app = QApplication(sys.argv)
    
    # 2. Configurar Estilo "Fusion" (Moderno y neutro)
    app.setStyle("Fusion")

    # 3. APLICAR TEMA OSCURO (DARK MODE)
    # Esto reemplaza al ctk.set_appearance_mode("Dark")
    palette = QPalette()
    
    # Colores base (Gris Azulado Oscuro - "Slate")
    palette.setColor(QPalette.Window, QColor(15, 23, 42))        # Fondo Ventana
    palette.setColor(QPalette.WindowText, Qt.white)              # Texto General
    palette.setColor(QPalette.Base, QColor(30, 41, 59))          # Fondo Inputs/Listas
    palette.setColor(QPalette.AlternateBase, QColor(51, 65, 85)) # Filas alternas
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)                    # Texto en inputs
    palette.setColor(QPalette.Button, QColor(51, 65, 85))        # Color Botones
    palette.setColor(QPalette.ButtonText, Qt.white)              # Texto Botones
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(59, 130, 246))        # Azul Enlaces/Accent
    palette.setColor(QPalette.Highlight, QColor(59, 130, 246))   # Selección (Azul)
    palette.setColor(QPalette.HighlightedText, Qt.white)
    
    app.setPalette(palette)

    # 4. Iniciar la Ventana Principal
    window = MainWindow()
    window.show() # Importante: En Qt la ventana es invisible por defecto
    
    # 5. Ejecutar el bucle principal
    sys.exit(app.exec())