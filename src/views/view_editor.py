import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                               QPushButton, QFrame, QLabel, QFileDialog, QToolBar,
                               QScrollArea, QMessageBox, QGraphicsDropShadowEffect)
from PySide6.QtGui import QTextCharFormat, QFont, QTextCursor, QTextListFormat, QColor, QAction
from PySide6.QtCore import Qt

class EditorView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        # --- ESTILOS VISUALES ---
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a; 
                color: #f1f5f9;
                font-family: 'Segoe UI', sans-serif;
            }
            
            /* BARRA SUPERIOR */
            QFrame#Toolbar {
                background-color: #1e293b;
                border-bottom: 1px solid #334155;
            }
            
            /* BOTONES HERRAMIENTAS */
            QPushButton.ToolBtn {
                background-color: transparent;
                border: 1px solid #475569;
                border-radius: 4px;
                padding: 5px 10px;
                color: #94a3b8;
                font-weight: bold;
            }
            QPushButton.ToolBtn:hover {
                background-color: #334155;
                color: white;
                border-color: #94a3b8;
            }
            QPushButton.ToolBtn:checked {
                background-color: #3b82f6;
                border-color: #3b82f6;
                color: white;
            }

            /* BARRA INFERIOR */
            QFrame#BottomBar {
                background-color: #1e293b;
                border-top: 1px solid #334155;
            }

            /* BOTONES ACCIÓN */
            QPushButton#BtnBack {
                background-color: transparent;
                border: 1px solid #64748b;
                color: #94a3b8;
                border-radius: 6px;
                padding: 8px 15px;
                font-weight: 600;
            }
            QPushButton#BtnBack:hover {
                color: white; border-color: white;
            }

            QPushButton#BtnSave {
                background-color: #8b5cf6; 
                border: none;
                color: white;
                border-radius: 6px;
                padding: 10px 30px;
                font-weight: 700;
                font-size: 14px;
            }
            QPushButton#BtnSave:hover {
                background-color: #7c3aed;
            }
        """)

        # --- LAYOUT PRINCIPAL ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. BARRA DE HERRAMIENTAS
        self.create_toolbar(main_layout)

        # 2. ÁREA DE EDICIÓN
        editor_container = QWidget()
        editor_container.setStyleSheet("background-color: #0f172a;") 
        container_layout = QVBoxLayout(editor_container)
        container_layout.setAlignment(Qt.AlignHCenter)
        container_layout.setContentsMargins(0, 20, 0, 0)

        # --- LA HOJA DE PAPEL ---
        self.editor = QTextEdit()
        self.editor.setFixedWidth(850)  # Ancho A4
        
        # ESTILO DIRECTO AL EDITOR (Blanco puro)
        self.editor.setStyleSheet("""
            QTextEdit {
                background-color: white;
                color: black;
                border: none;
                padding: 50px;
                font-family: 'Times New Roman', serif;
                font-size: 14px;
            }
            QScrollBar:vertical {
                background: #f1f5f9; width: 12px; margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1; min-height: 20px; border-radius: 6px;
            }
        """)
        
        # Sombra
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25); shadow.setXOffset(0); shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.editor.setGraphicsEffect(shadow)
        
        container_layout.addWidget(self.editor)
        main_layout.addWidget(editor_container)

        # 3. BARRA INFERIOR
        bottom_bar = QFrame(); bottom_bar.setObjectName("BottomBar")
        bl = QHBoxLayout(bottom_bar)
        bl.setContentsMargins(30, 15, 30, 15)

        btn_back = QPushButton("❮  Volver / Editar Datos")
        btn_back.setObjectName("BtnBack")
        btn_back.setCursor(Qt.PointingHandCursor)
        btn_back.clicked.connect(self.go_back)
        bl.addWidget(btn_back)

        bl.addStretch() 

        btn_save = QPushButton("💾  GUARDAR DOCUMENTO WORD (.docx)")
        btn_save.setObjectName("BtnSave")
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.clicked.connect(self.export_document)
        bl.addWidget(btn_save)

        bl.addStretch() 

        dummy_spacer = QFrame(); dummy_spacer.setFixedWidth(100); dummy_spacer.setStyleSheet("background: transparent;")
        bl.addWidget(dummy_spacer)
        
        main_layout.addWidget(bottom_bar)

    def create_toolbar(self, layout):
        tb = QFrame(); tb.setObjectName("Toolbar")
        l = QHBoxLayout(tb); l.setContentsMargins(20, 10, 20, 10); l.setSpacing(15)
        
        l.addWidget(QLabel("EDITOR DE LICITACIÓN", styleSheet="font-weight:900; color:#f8fafc; font-size:16px; margin-right:15px;"))
        
        self.btn_b = self.tool_btn("B", self.text_bold); self.btn_b.setToolTip("Negrita"); l.addWidget(self.btn_b)
        self.btn_i = self.tool_btn("I", self.text_italic); self.btn_i.setToolTip("Cursiva"); l.addWidget(self.btn_i)
        self.btn_u = self.tool_btn("U", self.text_underline); self.btn_u.setToolTip("Subrayado"); l.addWidget(self.btn_u)
        
        sep = QFrame(); sep.setFrameShape(QFrame.VLine); sep.setStyleSheet("background-color: #475569; width: 1px;"); sep.setFixedHeight(20)
        l.addWidget(sep)
        
        l.addWidget(self.tool_btn("• Lista", self.list_bullet))
        l.addWidget(self.tool_btn("1. Num", self.list_num))

        sep2 = QFrame(); sep2.setFrameShape(QFrame.VLine); sep2.setStyleSheet("background-color: #475569; width: 1px;"); sep2.setFixedHeight(20)
        l.addWidget(sep2)

        btn_minus = QPushButton("A-"); btn_minus.setProperty("class", "ToolBtn"); btn_minus.setCursor(Qt.PointingHandCursor)
        btn_minus.clicked.connect(lambda: self.change_font_size(-1))
        l.addWidget(btn_minus)

        btn_plus = QPushButton("A+"); btn_plus.setProperty("class", "ToolBtn"); btn_plus.setCursor(Qt.PointingHandCursor)
        btn_plus.clicked.connect(lambda: self.change_font_size(1))
        l.addWidget(btn_plus)
        
        l.addStretch()
        layout.addWidget(tb)

    def tool_btn(self, txt, func):
        b = QPushButton(txt); b.setProperty("class", "ToolBtn"); b.setCheckable(True)
        b.setCursor(Qt.PointingHandCursor); b.clicked.connect(func); return b

    # --- FUNCIONES DE FORMATO ---
    def text_bold(self): self.merge_fmt(QTextCharFormat(), 'bold')
    def text_italic(self): self.merge_fmt(QTextCharFormat(), 'italic')
    def text_underline(self): self.merge_fmt(QTextCharFormat(), 'underline')
    def list_bullet(self): self.editor.textCursor().createList(QTextListFormat.ListDisc)
    def list_num(self): self.editor.textCursor().createList(QTextListFormat.ListDecimal)
    
    def change_font_size(self, delta):
        cursor = self.editor.textCursor()
        fmt = cursor.charFormat()
        current_size = fmt.fontPointSize()
        if current_size <= 0: current_size = 14.0 
        new_size = current_size + delta
        if new_size < 8: new_size = 8
        if new_size > 72: new_size = 72
        fmt.setFontPointSize(new_size)
        self.merge_fmt(fmt, 'size')

    def merge_fmt(self, fmt, type):
        cursor = self.editor.textCursor()
        if type == 'bold': fmt.setFontWeight(QFont.Bold if self.btn_b.isChecked() else QFont.Normal)
        if type == 'italic': fmt.setFontItalic(self.btn_i.isChecked())
        if type == 'underline': fmt.setFontUnderline(self.btn_u.isChecked())
        cursor.mergeCharFormat(fmt); self.editor.mergeCurrentCharFormat(fmt); self.editor.setFocus()

    # --- ESTA ES LA FUNCIÓN CLAVE QUE FALTABA ---
    # Se llama load_data_variables porque así la invoca tu MainWindow
    def load_data_variables(self):
        d = self.controller.current_session.get("data", {})
        
        # CSS (Títulos corregidos: Subtítulos pequeños, Título grande)
        css = """
        <style>
            body { font-family: 'Times New Roman', serif; font-size: 14px; line-height: 1.2; color: #000000; }
            
            h1 { text-align: center; font-size: 16px; font-weight: bold; margin-top: 20px; margin-bottom: 5px; text-transform: uppercase; color: #000; }
            
            /* SUBTÍTULOS (Bases Adm/Tecnicas): 12px */
            h1.subtitle { 
                margin-top: 0px; margin-bottom: 20px; 
                font-size: 12px; 
                font-weight: bold; 
                text-align: center;
                text-transform: uppercase;
                color: #000; 
            } 
            
            h2 { font-size: 14px; font-weight: bold; margin-top: 20px; margin-bottom: 10px; text-transform: uppercase; text-decoration: underline; color: #000; }
            
            p { margin-bottom: 10px; text-align: justify; color: #000; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 15px; font-size: 13px; color: #000; }
            td, th { border: 1px solid black; padding: 5px; vertical-align: top; }
            .th-gray { background-color: #f2f2f2; font-weight: bold; }
            ul { margin-top: 5px; margin-bottom: 10px; color: #000; }
            li { margin-bottom: 5px; }
        </style>
        """

        # HTML
        html = f"{css}<body>"
        html += f"<h1>LICITACIÓN {d.get('nombre_adquisicion', '').upper()}</h1>"
        html += f"<h1 class='subtitle'>BASES ADMINISTRATIVAS</h1>" 
        html += f"<p><strong>{d.get('organismo','')}</strong>, en adelante “la Isapre”, invita a empresas...</p>"

        # CARACTERÍSTICAS
        if d.get('check_caracteristicas_de_la_licitacion', 1):
            html += """<h2>CARACTERÍSTICAS DE LA LICITACIÓN</h2>
            <table>
                <tr><td class='th-gray'>Razón Social</td><td>""" + str(d.get('razon_social','')) + """</td></tr>
                <tr><td class='th-gray'>RUT</td><td>""" + str(d.get('rut_empresa','')) + """</td></tr>
                <tr><td class='th-gray'>Comuna</td><td>""" + str(d.get('comuna','')) + """</td></tr>
                <tr><td class='th-gray'>Región</td><td>""" + str(d.get('region','')) + """</td></tr>
                <tr><td class='th-gray'>Nombre de Adquisición</td><td>""" + str(d.get('nombre_adquisicion','')) + """</td></tr>
                <tr><td class='th-gray'>Descripción</td><td>""" + str(d.get('descripcion','')) + """</td></tr>
                <tr><td class='th-gray'>Duración de contrato</td><td>""" + str(d.get('duracion_contrato','')) + """</td></tr>
                <tr><td class='th-gray'>Tipo de licitación</td><td>""" + str(d.get('tipo_licitacion','')) + """</td></tr>
                <tr><td class='th-gray'>Moneda</td><td>""" + str(d.get('moneda','')) + """</td></tr>
            </table>"""

        # CLÁUSULAS
        clauses = [
            ("OBJETIVOS", "check_objetivos"), ("DEFINICIONES", "check_definiciones"),
            ("ORDEN DE PRECEDENCIA DE LOS DOCUMENTOS", "check_orden_de_precedencia_de_los_documentos"),
            ("CONTENIDO DE LAS BASES", "check_contenido_de_las_bases"), ("PLAZOS", "check_plazos"),
            ("REQUISITOS DE LOS OFERENTES", "check_requisitos_de_los_oferentes"),
            ("DURACIÓN Y FORMALIZACIÓN DE LA COMPRA", "check_duracion_y_formalizacion_de_la_compra"),
            ("NOTIFICACIONES", "check_notificaciones"),
            ("LLAMADO A PROPUESTA Y ENTREGA DE BASES", "check_llamado_a_propuesta_y_entrega_de_bases"),
            ("CONSULTAS, ACLARACIONES Y MODIFICACIONES", "check_consultas_aclaraciones_y_modificaciones"),
            ("PRESENTACIÓN DE LAS PROPUESTAS", "check_presentacion_de_las_propuestas"),
            ("ENTREGA DE LAS PROPUESTAS", "check_entrega_de_las_propuestas"),
            ("APERTURA DE LAS PROPUESTAS", "check_apertura_de_las_propuestas"),
            ("ADMISIBILIDAD DE LA PROPUESTA", "check_admisibilidad_de_la_propuesta"),
            ("ACLARACIONES", "check_aclaraciones"), ("VALIDEZ DE LA PROPUESTA", "check_validez_de_la_propuesta"),
            ("COMISIÓN DE EVALUACIÓN DE LAS OFERTAS", "check_comision_de_evaluacion_de_las_ofertas")
        ]
        for t, k in clauses:
            if d.get(k): html += f"<h2>{t}</h2><p>[Texto estándar de la cláusula {t}...]</p>"

        # GARANTÍAS
        if d.get('check_garantias', 1):
            html += f"""<h2>GARANTÍAS</h2>
            <p><b>Seriedad de la Oferta:</b></p>
            <table>
                <tr><td class='th-gray'>Tipo Documento</td><td>Boleta de Garantía...</td></tr>
                <tr><td class='th-gray'>Beneficiario</td><td>{d.get('organismo','')}</td></tr>
                <tr><td class='th-gray'>Rut</td><td>{d.get('rut_empresa','')}</td></tr>
                <tr><td class='th-gray'>Vencimiento</td><td>{d.get('vencimiento_seriedad','')}</td></tr>
                <tr><td class='th-gray'>Monto</td><td>${d.get('monto_seriedad','')}</td></tr>
                <tr><td class='th-gray'>Glosa</td><td>Para garantizar la seriedad...</td></tr>
            </table>
            <p><b>Fiel Cumplimiento:</b></p>
            <table>
                <tr><td class='th-gray'>Tipo Documento</td><td>Boleta de Garantía...</td></tr>
                <tr><td class='th-gray'>Beneficiario</td><td>{d.get('organismo','')}</td></tr>
                <tr><td class='th-gray'>Rut</td><td>{d.get('rut_empresa','')}</td></tr>
                <tr><td class='th-gray'>Vencimiento</td><td>{d.get('vencimiento_cumplimiento','')}</td></tr>
                <tr><td class='th-gray'>Monto</td><td>${d.get('monto_cumplimiento','')}</td></tr>
                <tr><td class='th-gray'>Glosa</td><td>Para garantizar el fiel cumplimiento...</td></tr>
            </table>"""

        # OTRAS CLÁUSULAS
        clauses_2 = [
            ("ACEPTACIÓN DE OFERTAS", "check_aceptacion_de_ofertas"), ("ADJUDICACIÓN", "check_adjudicacion"),
            ("SUSCRIPCIÓN DEL CONTRATO", "check_suscripcion_del_contrato"), ("DOMICILIO", "check_domicilio"),
            ("TERMINACIÓN ANTICIPADA DEL CONTRATO", "check_terminacion_anticipada_del_contrato"),
            ("SOLUCIÓN DE LAS CONTROVERSIAS", "check_solucion_de_las_controversias"),
            ("LUGAR Y UNIDAD DE TIEMPO EN QUE SE PRESTAN LOS SERVICIOS", "check_lugar_y_unidad_de_tiempo_en_que_se_prestan_los_servicios"),
            ("SANCIONES POR INCUMPLIMIENTO", "check_sanciones_por_incumplimiento"),
            ("OBLIGACIÓN DE RESERVA Y USO DE INFORMACIÓN", "check_obligacion_de_reserva_y_uso_de_informacion"),
            ("CONDICIONES DE PAGO Y FACTURACIÓN", "check_forma_de_pago__condiciones_de_pago_y_facturacion"),
            ("RESPONSABILIDAD", "check_responsabilidad")
        ]
        for t, k in clauses_2:
            if d.get(k): html += f"<h2>{t}</h2><p>[Texto estándar de la cláusula {t}...]</p>"

        # EVALUACIÓN
        if d.get('check_evaluacion_y_adjudicacion_de_las_ofertas', 1):
            dyn = ""
            if d.get('otros_criterios'):
                for l in str(d.get('otros_criterios','')).split('\n'):
                    if l.strip(): dyn += f"<li>{l.replace('-','').strip()}</li>"
            html += f"""<h2>EVALUACIÓN Y ADJUDICACIÓN DE LAS OFERTAS</h2>
            <p>Ponderación de Criterios:</p>
            <ul>
                <li>Oferta Económica: {d.get('eval_economica','0')}%</li>
                <li>Oferta Técnica: {d.get('eval_tecnica','0')}%</li>
                <li>Antecedentes y Experiencia: {d.get('eval_experiencia','0')}%</li>
                {dyn}
            </ul>
            <p>Adjudicación: se adjudicará a la oferta con mayor puntaje total.</p>"""

        html += """<h2>MODELO DE PREVENCIÓN DE DELITOS (LEY N° 20.393)</h2>
        <p>El adjudicatario declara conocer...</p>
        
        <h1 class='subtitle'>BASES TÉCNICAS</h1>
        
        <p>[Aquí se insertarán las especificaciones técnicas...]</p>
        
        <h2>ANEXO N°1: CALENDARIO DE LA PROPUESTA</h2>
        <table><tr><th class='th-gray'>ACTIVIDAD</th><th class='th-gray'>FECHA</th></tr><tr><td>...</td><td>...</td></tr></table>
        
        <h2>ANEXO N°2: FORMULARIO DE DATOS DEL OFERENTE</h2>
        <table><tr><td>Datos...</td></tr></table>
        
        <h2>ANEXO 3: OFERTA ECONÓMICA</h2>
        <table><tr><td>Precios...</td></tr></table>
        
        <h2>ANEXO 4: EXPERIENCIA</h2>
        <table><tr><td>Clientes...</td></tr></table>
        
        <h2>ANEXO 5: CUESTIONARIO BASE</h2>
        <p>[Cuestionario...]</p>
        
        <h2>ANEXO 6: ACUERDO DE CONFIDENCIALIDAD</h2>
        <p>Firmas...</p>
        
        <h2>ANEXO 7: EQUIPO DE TRABAJO</h2>
        <table><tr><td>Personal...</td></tr></table>
        
        <h2>ANEXO 8: ACTA DE RECEPCIÓN CONFORME</h2>
        <p>Firmas finales...</p>
        """
        
        html += "</body>"
        self.editor.setHtml(html)

    def export_document(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Licitación", "Licitacion_Generada.docx", "Word Files (*.docx)")
        if file_path:
            success = self.controller.generate_docx(file_path)
            if success: QMessageBox.information(self, "Éxito", f"Documento guardado en:\n{file_path}")
            else: QMessageBox.critical(self, "Error", "No se pudo generar el documento.")

    def go_back(self):
        self.controller.cambiar_vista("form")