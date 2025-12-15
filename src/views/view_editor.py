import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                               QPushButton, QFrame, QLabel, QFileDialog, QMessageBox, QGraphicsDropShadowEffect)
from PySide6.QtGui import QTextCharFormat, QFont, QTextListFormat, QColor
from PySide6.QtCore import Qt
from src.data.base_texts import TEXTOS_LEGALES

class EditorView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        self.setStyleSheet("""
            QWidget { background-color: #0f172a; color: #f1f5f9; font-family: 'Segoe UI'; }
            QFrame#Toolbar, QFrame#BottomBar { background-color: #1e293b; border: 1px solid #334155; }
            QPushButton.ToolBtn { background: transparent; border: 1px solid #475569; border-radius: 4px; color: #94a3b8; font-weight: bold; padding: 5px; }
            QPushButton.ToolBtn:checked { background: #3b82f6; color: white; border-color: #3b82f6; }
            QPushButton#BtnSave { background-color: #10b981; color: white; border-radius: 6px; font-weight: bold; }
            QPushButton#BtnExport { background-color: #8b5cf6; color: white; border-radius: 6px; font-weight: bold; }
        """)
        
        layout = QVBoxLayout(self); layout.setContentsMargins(0,0,0,0)
        self.create_toolbar(layout)
        
        container = QWidget(); cl = QVBoxLayout(container); cl.setAlignment(Qt.AlignHCenter)
        self.editor = QTextEdit(); self.editor.setFixedWidth(850)
        
        self.editor.setStyleSheet("""
            QTextEdit { 
                background-color: white; color: black; border: none; padding: 60px; 
                font-family: 'Times New Roman', serif; font-size: 14px; 
                line-height: 1.5;
            }
        """)
        shadow = QGraphicsDropShadowEffect(self); shadow.setBlurRadius(20); shadow.setColor(QColor(0,0,0,80))
        self.editor.setGraphicsEffect(shadow)
        cl.addWidget(self.editor); layout.addWidget(container)
        
        bar = QFrame(); bar.setObjectName("BottomBar"); bl = QHBoxLayout(bar); bl.setContentsMargins(20,10,20,10)
        b_back = QPushButton("❮ Volver"); b_back.clicked.connect(self.go_back); bl.addWidget(b_back); bl.addStretch()
        b_save = QPushButton("💾 Guardar Progreso"); b_save.setObjectName("BtnSave"); b_save.setFixedSize(160,40); b_save.clicked.connect(self.save_progress); bl.addWidget(b_save)
        b_exp = QPushButton("📄 Exportar Word"); b_exp.setObjectName("BtnExport"); b_exp.setFixedSize(160,40); b_exp.clicked.connect(self.export_doc); bl.addWidget(b_exp)
        layout.addWidget(bar)

    def create_toolbar(self, layout):
        tb = QFrame(); tb.setObjectName("Toolbar"); hl = QHBoxLayout(tb)
        hl.addWidget(QLabel("EDITOR", styleSheet="font-weight:bold; font-size:16px; margin-right:10px"))
        self.btn_b = self.tool_btn("B", lambda: self.fmt('b')); hl.addWidget(self.btn_b)
        self.btn_i = self.tool_btn("I", lambda: self.fmt('i')); hl.addWidget(self.btn_i)
        self.btn_u = self.tool_btn("U", lambda: self.fmt('u')); hl.addWidget(self.btn_u)
        hl.addWidget(self.tool_btn("• Lista", lambda: self.editor.textCursor().createList(QTextListFormat.ListDisc)))
        hl.addStretch(); layout.addWidget(tb)

    def tool_btn(self, t, f):
        b = QPushButton(t); b.setProperty("class","ToolBtn"); b.setCheckable(True); b.clicked.connect(f); return b
    def fmt(self, t):
        c = self.editor.textCursor(); f = c.charFormat()
        if t=='b': f.setFontWeight(QFont.Bold if self.btn_b.isChecked() else QFont.Normal)
        if t=='i': f.setFontItalic(self.btn_i.isChecked())
        if t=='u': f.setFontUnderline(self.btn_u.isChecked())
        c.mergeCharFormat(f); self.editor.mergeCurrentCharFormat(f); self.editor.setFocus()

    def load_data_variables(self):
        d = self.controller.current_session.get("data", {})
        if d.get("html_editado"): self.editor.setHtml(d.get("html_editado")); return

        SECCIONES = [
            "CARACTERÍSTICAS DE LA LICITACIÓN", "OBJETIVOS", "DEFINICIONES", 
            "ORDEN DE PRECEDENCIA DE LOS DOCUMENTOS", "CONTENIDO DE LAS BASES", "PLAZOS", 
            "REQUISITOS DE LOS OFERENTES", "DURACIÓN Y FORMALIZACIÓN DE LA COMPRA", "NOTIFICACIONES", 
            "LLAMADO A PROPUESTA Y ENTREGA DE BASES", "CONSULTAS, ACLARACIONES Y MODIFICACIONES", 
            "PRESENTACIÓN DE LAS PROPUESTAS", "ENTREGA DE LAS PROPUESTAS", "APERTURA DE LAS PROPUESTAS", 
            "ADMISIBILIDAD DE LA PROPUESTA", "ACLARACIONES", "VALIDEZ DE LA PROPUESTA", 
            "COMISIÓN DE EVALUACIÓN DE LAS OFERTAS", "GARANTÍAS", "ACEPTACIÓN DE OFERTAS", 
            "ADJUDICACIÓN", "SUSCRIPCIÓN DEL CONTRATO", "DOMICILIO", "TERMINACIÓN ANTICIPADA DEL CONTRATO", 
            "SOLUCIÓN DE LAS CONTROVERSIAS", "LUGAR Y UNIDAD DE TIEMPO EN QUE SE PRESTAN LOS SERVICIOS",
            "SANCIONES POR INCUMPLIMIENTO", "OBLIGACIÓN DE RESERVA Y USO DE INFORMACIÓN", 
            "FORMA DE PAGO / CONDICIONES DE PAGO Y FACTURACIÓN", "RESPONSABILIDAD", 
            "EVALUACIÓN Y ADJUDICACIÓN DE LAS OFERTAS"
        ]

        css = """<style>
            body { font-family: 'Times New Roman', serif; font-size: 14px; color: #000; line-height: 1.2; }
            h1 { text-align: center; font-size: 16px; margin: 20px 0; text-transform: uppercase; color: black; }
            h2 { font-size: 14px; margin-top: 20px; text-transform: uppercase; text-decoration: none; font-weight: bold; color: black; }
            p { margin-bottom: 10px; text-align: justify; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 15px; font-size: 14px; }
            td, th { border: 1px solid black; padding: 5px; vertical-align: top; }
            .th-gray { background-color: #f2f2f2; font-weight: bold; width: 30%; }
            .th-head { background-color: #e5e7eb; font-weight: bold; text-align: center; }
        </style>"""
        
        html = f"{css}<body><h1>LICITACIÓN {d.get('nombre_adquisicion','').upper()}</h1>"
        html += f"<p><strong>{d.get('organismo','')}</strong> invita a participar...</p>"

        for titulo in SECCIONES:
            k = "check_" + titulo.lower().replace(" ","_").replace(",","").replace(".","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("/","_")
            
            if d.get(k, 0):
                html += f"<h2>{titulo}</h2>"
                
                if titulo == "CARACTERÍSTICAS DE LA LICITACIÓN":
                    html += f"""<table>
                        <tr><td class='th-gray'>Razón Social</td><td>{d.get('razon_social','')}</td></tr>
                        <tr><td class='th-gray'>RUT</td><td>{d.get('rut_empresa','')}</td></tr>
                        <tr><td class='th-gray'>Comuna</td><td>{d.get('comuna','')}</td></tr>
                        <tr><td class='th-gray'>Región</td><td>{d.get('region','')}</td></tr>
                        <tr><td class='th-gray'>Nombre</td><td>{d.get('nombre_adquisicion','')}</td></tr>
                        <tr><td class='th-gray'>Descripción</td><td>{d.get('descripcion','')}</td></tr>
                        <tr><td class='th-gray'>Duración</td><td>{d.get('duracion_contrato','')}</td></tr>
                        <tr><td class='th-gray'>Tipo</td><td>{d.get('tipo_licitacion','')}</td></tr>
                        <tr><td class='th-gray'>Moneda</td><td>{d.get('moneda','')}</td></tr>
                    </table>"""
                elif titulo == "GARANTÍAS":
                    html += f"""<p><b>Seriedad de la Oferta:</b></p><table>
                        <tr><td class='th-gray'>Monto</td><td>${d.get('monto_seriedad','')}</td></tr>
                        <tr><td class='th-gray'>Vencimiento</td><td>{d.get('vencimiento_seriedad','')}</td></tr>
                        <tr><td class='th-gray'>Glosa</td><td>Garantía de seriedad.</td></tr>
                    </table>
                    <p><b>Fiel Cumplimiento:</b></p><table>
                        <tr><td class='th-gray'>Monto</td><td>${d.get('monto_cumplimiento','')}</td></tr>
                        <tr><td class='th-gray'>Vencimiento</td><td>{d.get('vencimiento_cumplimiento','')}</td></tr>
                        <tr><td class='th-gray'>Glosa</td><td>Garantía de cumplimiento.</td></tr>
                    </table>"""
                elif titulo == "EVALUACIÓN Y ADJUDICACIÓN DE LAS OFERTAS":
                    items_extra = ""
                    if d.get('otros_criterios'):
                        for l in str(d.get('otros_criterios','')).split('\n'):
                            if l.strip(): items_extra += f"<li>{l.replace('-','').strip()}</li>"
                    html += f"""<p>Ponderación:</p><ul><li>Económica: {d.get('eval_economica','0')}%</li><li>Técnica: {d.get('eval_tecnica','0')}%</li><li>Experiencia: {d.get('eval_experiencia','0')}%</li>{items_extra}</ul>"""
                else:
                    txt = TEXTOS_LEGALES.get(titulo, ""); 
                    try: txt = txt.format(**d)
                    except: pass
                    html += f"<div>{txt}</div>"

        # --- CALENDARIO 4 COLUMNAS ---
        cal_rows = ""
        for item in d.get("calendario", []):
            cal_rows += f"<tr><td>{item.get('actividad','')}</td><td>{item.get('inicio','')}</td><td>{item.get('termino','')}</td><td>{item.get('obs','')}</td></tr>"

        html += f"""
        <br>
        <h1 class='subtitle'>BASES TÉCNICAS</h1>
        <p>[Especificaciones Técnicas...]</p>
        
        <h2>ANEXO N°1: CALENDARIO DE LA PROPUESTA</h2>
        <table>
            <tr><th class='th-head'>ACTIVIDAD</th><th class='th-head'>INICIO</th><th class='th-head'>TÉRMINO</th><th class='th-head'>OBSERVACIÓN</th></tr>
            {cal_rows}
        </table>
        <br><hr><p style='text-align:center; color:gray;'>Fin del Documento</p>
        </body>"""
        
        self.editor.setHtml(html)

    def save_progress(self):
        self.controller.current_session["data"]["html_editado"] = self.editor.toHtml()
        self.controller.save_session_data(self.controller.current_session["data"])
        QMessageBox.information(self, "Guardado", "Progreso guardado.")
    def export_doc(self):
        fp, _ = QFileDialog.getSaveFileName(self, "Exportar", "Licitacion.docx", "Word (*.docx)")
        if fp: 
            if self.controller.generate_docx(fp): QMessageBox.information(self, "Éxito", f"Guardado en:\n{fp}")
    def go_back(self): self.controller.cambiar_vista("form")