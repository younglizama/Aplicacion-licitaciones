from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                               QFrame, QHBoxLayout)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QCursor

class WelcomeView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        # --- COLORES (Copiados de tu versión anterior) ---
        self.COLORS = {
            "bg_main": "#0f172a",
            "card_bg": "#1e293b",
            "accent": "#3b82f6",
            "accent_hover": "#2563eb",
            "text": "#f8fafc",
            "text_gray": "#94a3b8",
            "btn_secondary": "#334155"
        }

        # Configuración del widget principal
        # En PySide no se usa 'configure(fg_color)', se usa setStyleSheet
        self.setStyleSheet(f"background-color: {self.COLORS['bg_main']};")
        
        self.place_content()

    def place_content(self):
        # Layout Principal (Vertical)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter) # Centrar todo verticalmente
        
        # --- TARJETA CENTRAL ---
        # Usamos QFrame en lugar de CTkFrame
        card = QFrame()
        card.setFixedSize(600, 450)
        
        # Estilos CSS (QSS) para replicar la apariencia de CustomTkinter
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

        # 1. Emoji
        lbl_emoji = QLabel("🚀")
        lbl_emoji.setStyleSheet("background-color: transparent; font-size: 60px;")
        lbl_emoji.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(lbl_emoji)
        card_layout.addSpacing(20) # Margen extra como pady=(40, 10)

        # 2. Título
        lbl_title = QLabel("Generador de Licitaciones")
        lbl_title.setStyleSheet(f"color: {self.COLORS['text']}; background-color: transparent; font-weight: bold; font-size: 32px; font-family: Roboto;")
        lbl_title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(lbl_title)

        # 3. Subtítulo
        lbl_desc = QLabel("Gestión inteligente de documentos.\nCrea, edita y administra tus licitaciones.")
        lbl_desc.setStyleSheet(f"color: {self.COLORS['text_gray']}; background-color: transparent; font-size: 14px; font-family: Roboto;")
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
                font-family: Roboto;
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
                font-family: Roboto;
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

        # 6. Footer (v2.1 ...)
        # Lo añadimos fuera de la tarjeta, en el layout principal
        lbl_footer = QLabel("v2.1 | Powered by Python")
        lbl_footer.setStyleSheet(f"color: #334155; font-size: 10px; font-family: Roboto;") # Usamos un color oscuro sutil
        lbl_footer.setAlignment(Qt.AlignCenter)
        
        main_layout.addSpacing(20)
        main_layout.addWidget(lbl_footer)

    def start_app(self):
        # Llama al método del MainWindow
        self.controller.start_new_licitacion()

    def go_history(self):
        # Llama al método de cambio de vista
        self.controller.cambiar_vista("files")