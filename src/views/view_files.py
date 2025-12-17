import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QTableWidget, QTableWidgetItem, 
                               QHeaderView, QMessageBox, QFrame, QFileDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush, QCursor, QFont

# Importamos el generador para poder "descargar/regenerar" el archivo en cualquier PC
from src.controllers.doc_generator import DocumentGenerator

class FilesView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        # Ruta de la plantilla para regenerar documentos si no existen
        self.TEMPLATE_PATH = os.path.join("assets", "templates", "plantilla_base.docx")
        
        # Fondo Principal
        self.setStyleSheet("background-color: #0f172a;") 
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ==========================================
        # 1. SIDEBAR (IZQUIERDA)
        # ==========================================
        sidebar = QFrame()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet("background-color: #1e293b; border-right: 1px solid #334155;")
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar_layout.setContentsMargins(20, 30, 20, 20)

        lbl_historial = QLabel("HISTORIAL")
        lbl_historial.setStyleSheet("color: white; font-weight: bold; font-size: 20px; border: none;")
        sidebar_layout.addWidget(lbl_historial)
        sidebar_layout.addSpacing(20)

        # BOTÓN 1: INICIO (Se mantiene)
        btn_home = QPushButton("🏠 Inicio")
        btn_home.setCursor(Qt.PointingHandCursor)
        btn_home.setFixedHeight(45)
        btn_home.setFont(QFont("Segoe UI Emoji", 12))
        btn_home.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6; color: white; border-radius: 6px;
                font-weight: bold; text-align: left; padding-left: 15px; font-size: 14px;
                border: none;
            }
            QPushButton:hover { background-color: #2563eb; }
        """)
        btn_home.clicked.connect(lambda: self.controller.cambiar_vista("welcome"))
        sidebar_layout.addWidget(btn_home)
        
        sidebar_layout.addSpacing(10)

        # BOTÓN 2: VOLVER AL FORMULARIO (Nuevo)
        btn_back_form = QPushButton("❮ Volver al Formulario")
        btn_back_form.setCursor(Qt.PointingHandCursor)
        btn_back_form.setFixedHeight(45)
        btn_back_form.setFont(QFont("Segoe UI Emoji", 12))
        btn_back_form.setStyleSheet("""
            QPushButton {
                background-color: #475569; color: #f8fafc; border-radius: 6px;
                font-weight: bold; text-align: left; padding-left: 15px; font-size: 14px;
                border: none;
            }
            QPushButton:hover { background-color: #64748b; }
        """)
        btn_back_form.clicked.connect(lambda: self.controller.cambiar_vista("form"))
        sidebar_layout.addWidget(btn_back_form)

        sidebar_layout.addStretch()

        # ==========================================
        # 2. CONTENIDO (DERECHA)
        # ==========================================
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(50, 40, 50, 40)
        content_layout.setSpacing(20)

        lbl_title = QLabel("Licitaciones Recientes")
        lbl_title.setStyleSheet("color: #f8fafc; font-size: 28px; font-weight: bold; border: none;")
        content_layout.addWidget(lbl_title)

        # --- CONTENEDOR DE LA TABLA (Para bordes redondeados perfectos) ---
        table_container = QFrame()
        # Overflow hidden es clave para que las esquinas de la tabla se recorten
        table_container.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border-radius: 12px;
                border: 1px solid #334155;
            }
        """)
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(0)

        # TABLA
        self.table = QTableWidget()
        self.setup_table_style()
        
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["FOLIO", "NOMBRE ADQUISICIÓN", "EMPRESA", "ESTADO", "ACCIONES"])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Folio
        header.setSectionResizeMode(1, QHeaderView.Stretch)          # Nombre (Estira para ocupar espacio)
        header.setSectionResizeMode(2, QHeaderView.Stretch)          # Empresa
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents) # Estado
        header.setSectionResizeMode(4, QHeaderView.Fixed)            # Acciones
        self.table.setColumnWidth(4, 340) 

        table_layout.addWidget(self.table)
        content_layout.addWidget(table_container)
        
        # Botón Actualizar (Abajo derecha)
        bottom_bar = QHBoxLayout()
        bottom_bar.addStretch() 
        
        btn_refresh = QPushButton("🔄 Actualizar Lista")
        btn_refresh.setFixedWidth(160)
        btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #334155; color: #94a3b8; border: none; 
                padding: 12px; border-radius: 4px; font-weight: bold; font-size: 13px;
            }
            QPushButton:hover { background-color: #475569; color: white; }
        """)
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.clicked.connect(self.load_history)
        
        bottom_bar.addWidget(btn_refresh)
        bottom_bar.addSpacing(80) 

        content_layout.addLayout(bottom_bar)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

        self.load_history()

    def setup_table_style(self):
        """Estilo suave y moderno"""
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.verticalHeader().setDefaultSectionSize(65) # Altura generosa de fila

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: transparent; /* Hereda del contenedor */
                color: #f1f5f9;
                border: none;
                font-size: 13px;
                gridline-color: transparent;
            }
            QHeaderView::section {
                background-color: #3b82f6; /* Header Azul */
                color: white;
                padding: 15px 20px; /* Padding extra para alinear texto */
                border: none;
                font-weight: bold;
                font-size: 13px;
                text-align: left;
            }
            QHeaderView::section:first { border-top-left-radius: 12px; }
            QHeaderView::section:last { border-top-right-radius: 12px; }
            
            QTableCornerButton::section { background-color: #3b82f6; border: none; }
            
            QTableWidget::item {
                padding-left: 20px; /* Mueve el texto a la derecha */
                padding-right: 10px;
                border-bottom: 1px solid #334155;
            }
            QTableWidget::item:selected {
                background-color: #1e3a8a; color: white;
            }
        """)

    def load_history(self):
        self.table.setRowCount(0)
        rows = self.controller.db.get_all_licitaciones()
        if not rows: return

        self.table.setRowCount(len(rows))

        for row_idx, data in enumerate(rows):
            # Alineación vertical centrada + Izquierda
            align_v = Qt.AlignVCenter | Qt.AlignLeft

            # 1. Folio
            id_txt = data["folio"] if data["folio"] else str(data["id"])
            item_id = QTableWidgetItem(id_txt)
            item_id.setForeground(QBrush(QColor("#3b82f6")))
            item_id.setTextAlignment(align_v)
            self.table.setItem(row_idx, 0, item_id)

            # 2. Nombre (Aseguramos que no quede vacío ni mal alineado)
            nombre_texto = data["nombre"] if data["nombre"] else "(Sin Nombre)"
            item_nombre = QTableWidgetItem(nombre_texto)
            item_nombre.setTextAlignment(align_v)
            self.table.setItem(row_idx, 1, item_nombre)
            
            # 3. Empresa
            item_empresa = QTableWidgetItem(data["empresa"])
            item_empresa.setForeground(QBrush(QColor("#cbd5e1")))
            item_empresa.setTextAlignment(align_v)
            self.table.setItem(row_idx, 2, item_empresa)

            # 4. Estado
            estado = data["estado"]
            item_estado = QTableWidgetItem(estado)
            if estado == "Generado":
                item_estado.setForeground(QBrush(QColor("#10b981"))) # Verde
            else:
                item_estado.setForeground(QBrush(QColor("gray")))
            item_estado.setTextAlignment(align_v)
            self.table.setItem(row_idx, 3, item_estado)

            # 5. Botones
            self.create_action_buttons(row_idx, data)

    def create_action_buttons(self, row_idx, data):
        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        layout = QHBoxLayout(container)
        layout.setAlignment(Qt.AlignCenter) 
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10) 

        def crear_boton(texto, color_bg, hover_color, callback):
            btn = QPushButton(texto)
            btn.setFixedSize(85, 34) # Botón grandecito
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{ 
                    background-color: {color_bg}; color: white; 
                    border-radius: 6px; border: none; font-weight: bold; font-size: 11px;
                }}
                QPushButton:hover {{ background-color: {hover_color}; }}
            """)
            btn.clicked.connect(callback)
            return btn

        # A. EDITAR (AHORA VA AL FORMULARIO, NO AL EDITOR)
        btn_edit = crear_boton("Editar", "#334155", "#475569", lambda: self.edit_licitacion(data))
        layout.addWidget(btn_edit)

        # B. DESCARGAR / WORD (Inteligente)
        # Siempre mostramos el botón. Si no existe localmente, lo regenera.
        btn_word = crear_boton("Word", "#059669", "#10b981", lambda: self.handle_word_action(data))
        layout.addWidget(btn_word)

        # C. BORRAR
        btn_del = crear_boton("Borrar", "#dc2626", "#ef4444", lambda: self.delete_licitacion(data))
        layout.addWidget(btn_del)

        self.table.setCellWidget(row_idx, 4, container)

    # --- LÓGICA DE DESCARGA INTELIGENTE ---
    def handle_word_action(self, data):
        ruta = data.get("ruta_archivo")
        
        # 1. Si existe el archivo en el PC, lo abrimos
        if ruta and os.path.exists(ruta):
            os.startfile(ruta)
        
        # 2. Si NO existe (cambio de PC), ofrecemos regenerarlo (Descargar)
        else:
            reply = QMessageBox.question(
                self, 
                "Archivo no encontrado", 
                "El archivo no está en la ruta original (quizás cambiaste de PC).\n¿Deseas descargar una copia nueva?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.regenerar_archivo(data)

    def regenerar_archivo(self, data):
        # Lógica para re-crear el Word desde la BD
        full_data = self.controller.db.get_licitacion_by_id(data["id"])
        if not full_data: return

        datos_json = full_data["datos_json"]
        
        # Pedir donde guardar
        nombre_sug = f"Licitacion_{datos_json.get('folio', 'Recuperada')}.docx"
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Copia", nombre_sug, "Word Document (*.docx)")
        
        if file_path:
            try:
                gen = DocumentGenerator(self.TEMPLATE_PATH)
                context = datos_json.copy()
                if "secciones_texto" in context:
                    for k, v in context["secciones_texto"].items():
                        # Limpiar HTML básico
                        clean_v = v.replace("<div>","").replace("</div>","\n").replace("<br>","\n")
                        context[k.replace(" ", "_")] = clean_v
                
                success, msg = gen.generar_word(context, file_path)
                
                if success:
                    # Actualizamos la nueva ruta en la BD para este PC
                    self.controller.db.guardar_licitacion({"ruta_archivo": file_path}, data["id"])
                    QMessageBox.information(self, "Éxito", "Archivo descargado correctamente.")
                    os.startfile(file_path)
                    self.load_history() # Refrescar para que el botón ahora apunte aquí
                else:
                    QMessageBox.critical(self, "Error", msg)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo generar: {str(e)}\nVerifica que la plantilla exista en assets/templates/")

    def edit_licitacion(self, data):
        full_data = self.controller.db.get_licitacion_by_id(data["id"])
        if full_data:
            self.controller.current_session["licitacion_id"] = full_data["id"]
            self.controller.current_session["data"] = full_data["datos_json"]
            # CAMBIO: Redirige a "form" en lugar de "editor"
            self.controller.cambiar_vista("form")

    def delete_licitacion(self, data):
        reply = QMessageBox.question(self, "Eliminar", f"¿Estás seguro de borrar '{data['nombre']}'?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.controller.db.delete_licitacion(data["id"])
            self.load_history()