import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                               QLabel, QFrame, QScrollArea, QLineEdit, 
                               QGraphicsDropShadowEffect, QApplication)
from PySide6.QtCore import Qt, QEvent, Signal, Slot
from PySide6.QtGui import QFont

# Importamos TU controlador nuevo
from src.controllers.chat_controller import ChatController

class ChatView(QWidget):
    # Definimos una "Señal" para comunicarnos desde el hilo de fondo a la interfaz
    ai_response_signal = Signal(str)

    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.parent = parent_window 
        self.chat_window = None
        self.is_open = False
        
        # --- 1. INICIAR CONTROLADOR ---
        try:
            self.controller = ChatController()
        except Exception as e:
            print(f"Error iniciando ChatController: {e}")
            self.controller = None

        # Conectamos la señal a la función que dibuja la burbuja
        self.ai_response_signal.connect(self.handle_ai_response_ui)

        # --- ESTILOS VISUALES ---
        self.STYLES = {
            "fab": """
                QPushButton {
                    background-color: #3b82f6; border-radius: 30px; 
                    color: white; font-size: 24px; border: 2px solid #1e293b;
                }
                QPushButton:hover { background-color: #2563eb; }
            """,
            "window": "background-color: #0f172a; border: 1px solid #334155;",
            "header": "background-color: #1e293b; border-bottom: 1px solid #334155;",
            "input_area": "background-color: #1e293b; border-top: 1px solid #334155;",
            "input": """
                QLineEdit {
                    background-color: #0f172a; color: white; border-radius: 20px;
                    padding: 8px 15px; border: 1px solid #334155;
                }
                QLineEdit:focus { border: 1px solid #3b82f6; }
            """
        }

        # --- CREAR BOTÓN FLOTANTE (FAB) ---
        self.fab = QPushButton("💬", self.parent)
        self.fab.setFixedSize(60, 60)
        self.fab.setStyleSheet(self.STYLES["fab"])
        self.fab.setCursor(Qt.PointingHandCursor)
        self.fab.clicked.connect(self.toggle_chat)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 4)
        self.fab.setGraphicsEffect(shadow)

        self.parent.installEventFilter(self)
        self.update_fab_position()

    # --- LÓGICA DE POSICIONAMIENTO ---
    def eventFilter(self, obj, event):
        if obj == self.parent and event.type() == QEvent.Resize:
            self.update_fab_position()
        return super().eventFilter(obj, event)

    def update_fab_position(self):
        new_x = self.parent.width() - 80
        new_y = self.parent.height() - 80
        self.fab.move(new_x, new_y)
        if self.is_open and self.chat_window:
            self.chat_window.move(self.parent.geometry().right() - 410, 
                                  self.parent.geometry().bottom() - 610)

    # --- LÓGICA DE VENTANA ---
    def toggle_chat(self):
        if self.is_open:
            self.close_chat()
        else:
            self.open_chat()

    def open_chat(self):
        self.is_open = True
        self.fab.setText("✖")
        self.fab.setStyleSheet(self.STYLES["fab"].replace("#3b82f6", "#ef4444").replace("#2563eb", "#dc2626"))

        self.chat_window = QWidget(self.parent)
        self.chat_window.setWindowFlags(Qt.SubWindow | Qt.FramelessWindowHint)
        self.chat_window.resize(380, 550)
        self.chat_window.setStyleSheet(self.STYLES["window"])
        
        self.chat_window.move(self.parent.width() - 400, self.parent.height() - 650)
        
        layout = QVBoxLayout(self.chat_window)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # HEADER
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet(self.STYLES["header"])
        header_layout = QHBoxLayout(header)
        
        lbl_title = QLabel("✨ Copiloto IA")
        lbl_title.setStyleSheet("color: white; font-weight: bold; font-size: 16px; border: none;")
        header_layout.addWidget(lbl_title)
        
        # Detectar modelo usado
        model_name = "Gemini"
        if self.controller and self.controller.model:
            model_name = self.controller.model.model_name.replace("models/", "")

        lbl_status = QLabel(f"● {model_name}")
        lbl_status.setStyleSheet("color: #4ade80; font-size: 12px; border: none;")
        header_layout.addWidget(lbl_status, 0, Qt.AlignRight)
        layout.addWidget(header)

        # MENSAJES
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none; background: transparent;")
        self.scroll_area.verticalScrollBar().setStyleSheet("background: #0f172a;")
        
        self.msg_container = QWidget()
        self.msg_container.setStyleSheet("background: transparent;")
        self.msg_layout = QVBoxLayout(self.msg_container)
        self.msg_layout.setAlignment(Qt.AlignTop)
        self.msg_layout.setSpacing(15)
        
        self.scroll_area.setWidget(self.msg_container)
        layout.addWidget(self.scroll_area)

        self.add_bubble("Hola 👋. Soy tu experto en Licitaciones. ¿En qué te ayudo?", is_user=False)

        # INPUT AREA
        footer = QFrame()
        footer.setFixedHeight(70)
        footer.setStyleSheet(self.STYLES["input_area"])
        footer_layout = QHBoxLayout(footer)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Escribe tu consulta...")
        self.input_field.setStyleSheet(self.STYLES["input"])
        self.input_field.returnPressed.connect(self.send_message)
        footer_layout.addWidget(self.input_field)

        btn_send = QPushButton("➤")
        btn_send.setFixedSize(40, 40)
        btn_send.setCursor(Qt.PointingHandCursor)
        btn_send.setStyleSheet("background-color: #3b82f6; border-radius: 20px; color: white; border: none;")
        btn_send.clicked.connect(self.send_message)
        footer_layout.addWidget(btn_send)

        layout.addWidget(footer)
        self.chat_window.show()
        self.chat_window.raise_()

    def close_chat(self):
        self.is_open = False
        self.fab.setText("💬")
        self.fab.setStyleSheet(self.STYLES["fab"])
        if self.chat_window:
            self.chat_window.close()
            self.chat_window = None

    # --- LÓGICA DE MENSAJES Y CONEXIÓN ---
    def send_message(self):
        text = self.input_field.text().strip()
        if not text: return
        
        # 1. Mostrar mensaje del usuario
        self.add_bubble(text, is_user=True)
        self.input_field.clear()
        
        # 2. Mostrar indicador de carga
        self.loading_label = QLabel("Escribiendo...")
        self.loading_label.setStyleSheet("color: #94a3b8; font-style: italic; margin-left: 10px; border: none;")
        self.msg_layout.addWidget(self.loading_label)

        # 3. Llamar al controlador (esto crea un hilo por debajo)
        if self.controller:
            # Pasamos nuestro método 'receive_response' como callback
            self.controller.get_response(text, self.receive_response_from_thread)
        else:
            self.handle_ai_response_ui("❌ Error: Controlador no inicializado.")

    def receive_response_from_thread(self, response_text):
        """
        Este método es llamado por el hilo secundario del controlador.
        NO podemos tocar la UI aquí directamente o la app crasheará.
        Usamos una SEÑAL para volver al hilo principal.
        """
        self.ai_response_signal.emit(response_text)

    @Slot(str)
    def handle_ai_response_ui(self, text):
        """Este método se ejecuta en el hilo principal de la UI"""
        # Borrar "Escribiendo..."
        if hasattr(self, 'loading_label') and self.loading_label:
            self.loading_label.deleteLater()
            self.loading_label = None
        
        self.add_bubble(text, is_user=False)

    def add_bubble(self, text, is_user):
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(10, 0, 10, 0)
        
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setMaximumWidth(260)
        bubble.setFont(QFont("Segoe UI", 10))
        # Seleccionable para copiar texto
        bubble.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        if is_user:
            bubble.setStyleSheet("""
                background-color: #3b82f6; color: white; 
                padding: 10px; border-radius: 15px; border-bottom-right-radius: 2px;
            """)
            row_layout.addStretch()
            row_layout.addWidget(bubble)
        else:
            bubble.setStyleSheet("""
                background-color: #334155; color: #f1f5f9; 
                padding: 10px; border-radius: 15px; border-bottom-left-radius: 2px;
            """)
            row_layout.addWidget(bubble)
            row_layout.addStretch()
            
        self.msg_layout.addWidget(row)
        
        # Auto-scroll
        QApplication.processEvents()
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())