import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                               QFrame, QHBoxLayout)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QCursor, QPixmap

class WelcomeView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        # --- COLORES ---
        self.COLORS = {
            "bg_main": "#0f172a",
            "card_bg": "#334155",
            "accent": "#3b82f6",
            "accent_hover": "#2563eb",
            "text": "#f8fafc",
            "text_gray": "#ffffff",
            "btn_secondary": "#4F78B1"
        }

        # Configuración del widget principal
        self.setStyleSheet(f"background-color: {self.COLORS['bg_main']};")
        
        self.place_content()

    def place_content(self):
        # Layout Principal (Vertical)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter) # Centrar todo verticalmente
        
        # --- TARJETA CENTRAL ---
        card = QFrame()
        card.setFixedSize(600, 480) # Un poco más alto para acomodar el logo
        
        # Estilos CSS (QSS)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {self.COLORS['card_bg']};
                border-radius: 20px;
            }}
        """)
        
        # Layout dentro de la tarjeta
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(10) # Espacio entre elementos

        # 1. IMAGEN / LOGO (Reemplazo del cohete)
        lbl_logo = QLabel()
        lbl_logo.setAlignment(Qt.AlignCenter)
        lbl_logo.setStyleSheet("background-color: transparent;")
        
        # Ruta de la imagen
        img_path = os.path.join("assets", "icons", "logo.png")
        
        if os.path.exists(img_path):
            # Cargar y escalar la imagen
            pixmap = QPixmap(img_path)
            # Escalar a una altura de 100px manteniendo la proporción (SmoothTransformation para mejor calidad)
            scaled_pixmap = pixmap.scaledToHeight(120, Qt.SmoothTransformation)
            lbl_logo.setPixmap(scaled_pixmap)
        else:
            # Fallback: Si no encuentra la imagen, muestra el cohete
            lbl_logo.setText("🚀")
            lbl_logo.setStyleSheet("background-color: transparent; font-size: 60px;")

        card_layout.addWidget(lbl_logo)
        card_layout.addSpacing(10)

        # 2. Título
        lbl_title = QLabel("Generador de Licitaciones")
        lbl_title.setStyleSheet(f"color: {self.COLORS['text']}; background-color: transparent; font-weight: bold; font-size: 32px; font-family: 'Segoe UI', Roboto, sans-serif;")
        lbl_title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(lbl_title)

        # 3. Subtítulo
        lbl_desc = QLabel("Gestión inteligente de documentos.\nCrea, edita y administra tus licitaciones.")
        lbl_desc.setStyleSheet(f"color: {self.COLORS['text_gray']}; background-color: transparent; font-size: 14px; font-family: 'Segoe UI', Roboto, sans-serif;")
        lbl_desc.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(lbl_desc)
        card_layout.addSpacing(30)

        # 4. Botón Nuevo (Estilo Accent)
        btn_new = QPushButton("Comenzar Nueva Licitación  ➜")
        btn_new.setFixedSize(280, 50)
        btn_new.setCursor(Qt.PointingHandCursor)
        btn_new.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.COLORS['accent']};
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                font-family: 'Segoe UI', Roboto, sans-serif;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {self.COLORS['accent_hover']};
            }}
        """)
        btn_new.clicked.connect(self.start_app)
        card_layout.addWidget(btn_new, 0, Qt.AlignCenter)

        # 5. Botón Historial (Estilo Outline/Secundario)
        btn_history = QPushButton("📂 Ver Historial y Archivos")
        btn_history.setFixedSize(280, 45)
        btn_history.setCursor(Qt.PointingHandCursor)
        btn_history.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {self.COLORS['text_gray']};
                border: 2px solid {self.COLORS['btn_secondary']};
                border-radius: 10px;
                font-size: 15px;
                font-weight: bold;
                font-family: 'Segoe UI', Roboto, sans-serif;
            }}
            QPushButton:hover {{
                background-color: {self.COLORS['btn_secondary']};
                color: white;
            }}
        """)
        btn_history.clicked.connect(self.go_history)
        card_layout.addWidget(btn_history, 0, Qt.AlignCenter)

        # Añadir la tarjeta al layout principal
        main_layout.addWidget(card)

        # 6. Footer
        lbl_footer = QLabel("v2.2 | Powered by Python")
        lbl_footer.setStyleSheet(f"color: #334155; font-size: 10px; font-family: 'Segoe UI', Roboto, sans-serif;")
        lbl_footer.setAlignment(Qt.AlignCenter)
        
        main_layout.addSpacing(20)
        main_layout.addWidget(lbl_footer)

    def start_app(self):
        # Llama al método del MainWindow
        self.controller.start_new_licitacion()

    def go_history(self):
        # Llama al método de cambio de vista
        self.controller.cambiar_vista("files")