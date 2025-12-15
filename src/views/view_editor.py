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
        l = QVBoxLayout(self); l.setContentsMargins(0,0,0,0)
        self.create_toolbar(l)
        c = QWidget(); cl = QVBoxLayout(c); cl.setAlignment(Qt.AlignHCenter)
        self.editor = QTextEdit(); self.editor.setFixedWidth(850)
        self.editor.setStyleSheet("QTextEdit { background: white; color: black; border: none; padding: 60px; font-family: 'Times New Roman'; font-size: 14px; line-height: 1.5; }")
        sh = QGraphicsDropShadowEffect(self); sh.setBlurRadius(20); sh.setColor(QColor(0,0,0,80)); self.editor.setGraphicsEffect(sh)
        cl.addWidget(self.editor); l.addWidget(c)
        b = QFrame(); b.setObjectName("BottomBar"); bl = QHBoxLayout(b); bl.setContentsMargins(20,10,20,10)
        bb = QPushButton("❮ Volver"); bb.clicked.connect(self.go_back); bl.addWidget(bb); bl.addStretch()
        bs = QPushButton("💾 Guardar Progreso"); bs.setObjectName("BtnSave"); bs.setFixedSize(160,40); bs.clicked.connect(self.save_progress); bl.addWidget(bs)
        be = QPushButton("📄 Exportar Word"); be.setObjectName("BtnExport"); be.setFixedSize(160,40); be.clicked.connect(self.export_doc); bl.addWidget(be)
        l.addWidget(b)

    def create_toolbar(self, l):
        t = QFrame(); t.setObjectName("Toolbar"); h = QHBoxLayout(t)
        h.addWidget(QLabel("EDITOR", styleSheet="font-weight:bold; font-size:16px; margin-right:10px"))
        self.btn_b = self.tool_btn("B", lambda: self.fmt('b')); h.addWidget(self.btn_b)
        self.btn_i = self.tool_btn("I", lambda: self.fmt('i')); h.addWidget(self.btn_i)
        self.btn_u = self.tool_btn("U", lambda: self.fmt('u')); h.addWidget(self.btn_u)
        h.addWidget(self.tool_btn("• Lista", lambda: self.editor.textCursor().createList(QTextListFormat.ListDisc)))
        h.addStretch(); l.addWidget(t)

    def tool_btn(self, t, f): b = QPushButton(t); b.setProperty("class","ToolBtn"); b.setCheckable(True); b.clicked.connect(f); return b
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
            "CARACTERÍSTICAS DE LA LICITACIÓN", "OBJETIVOS", "DEFINICIONES", "ORDEN DE PRECEDENCIA DE LOS DOCUMENTOS", "CONTENIDO DE LAS BASES", "PLAZOS", 
            "REQUISITOS DE LOS OFERENTES", "DURACIÓN Y FORMALIZACIÓN DE LA COMPRA", "NOTIFICACIONES", "LLAMADO A PROPUESTA Y ENTREGA DE BASES", "CONSULTAS, ACLARACIONES Y MODIFICACIONES", 
            "PRESENTACIÓN DE LAS PROPUESTAS", "ENTREGA DE LAS PROPUESTAS", "APERTURA DE LAS PROPUESTAS", "ADMISIBILIDAD DE LA PROPUESTA", "ACLARACIONES", "VALIDEZ DE LA PROPUESTA", 
            "COMISIÓN DE EVALUACIÓN DE LAS OFERTAS", "GARANTÍAS", "ACEPTACIÓN DE OFERTAS", "ADJUDICACIÓN", "SUSCRIPCIÓN DEL CONTRATO", "DOMICILIO", "TERMINACIÓN ANTICIPADA DEL CONTRATO", 
            "SOLUCIÓN DE LAS CONTROVERSIAS", "LUGAR Y UNIDAD DE TIEMPO EN QUE SE PRESTAN LOS SERVICIOS", "SANCIONES POR INCUMPLIMIENTO", "OBLIGACIÓN DE RESERVA Y USO DE INFORMACIÓN", 
            "FORMA DE PAGO / CONDICIONES DE PAGO Y FACTURACIÓN", "RESPONSABILIDAD", "EVALUACIÓN Y ADJUDICACIÓN DE LAS OFERTAS", "BASES TÉCNICAS"
        ]

        css = "<style>body{font-family:'Times New Roman';font-size:14px;line-height:1.2;color:#000}h1{text-align:center;font-size:16px;margin:20px 0}h2{font-size:14px;margin-top:20px;font-weight:bold}table{width:100%;border-collapse:collapse;margin-bottom:15px}td,th{border:1px solid black;padding:5px}.th-gray{background:#f2f2f2;font-weight:bold;width:30%}.th-head{background:#e5e7eb;font-weight:bold;text-align:center}</style>"
        h = f"{css}<body><h1>LICITACIÓN {d.get('nombre_adquisicion','').upper()}</h1><p><strong>{d.get('organismo','')}</strong> invita a participar...</p>"

        for t in SECCIONES:
            k = "check_" + t.lower().replace(" ","_").replace(",","").replace(".","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("/","_")
            if d.get(k, 0):
                h += f"<h2>{t}</h2>"
                if t == "CARACTERÍSTICAS DE LA LICITACIÓN":
                    h += f"<table><tr><td class='th-gray'>Razón Social</td><td>{d.get('razon_social','')}</td></tr><tr><td class='th-gray'>RUT</td><td>{d.get('rut_empresa','')}</td></tr><tr><td class='th-gray'>Nombre</td><td>{d.get('nombre_adquisicion','')}</td></tr><tr><td class='th-gray'>Duración</td><td>{d.get('duracion_contrato','')}</td></tr></table>"
                elif t == "GARANTÍAS":
                    h += f"<p><b>Seriedad:</b> ${d.get('monto_seriedad','')}</p><p><b>Cumplimiento:</b> ${d.get('monto_cumplimiento','')}</p>"
                elif t == "EVALUACIÓN Y ADJUDICACIÓN DE LAS OFERTAS":
                    eco, tec, leg = d.get('eval_economica','0'), d.get('eval_tecnica','0'), d.get('eval_experiencia','0')
                    h += f"<ul><li>Económica: {eco}%</li><li>Técnica: {tec}%</li><li>Antecedentes Legales: {leg}%</li>"
                    if d.get('extra_criteria'):
                        for c in d.get('extra_criteria'): h += f"<li>{c['name']}: {c['pct']}%</li>"
                    h += "</ul>"
                else:
                    txt = TEXTOS_LEGALES.get(t, ""); 
                    try: txt = txt.format(**d)
                    except: pass
                    h += f"<div>{txt}</div>"

        # Calendario 4 columnas
        cr=""
        for i in d.get("calendario",[]): cr+=f"<tr><td>{i['actividad']}</td><td>{i['inicio']}</td><td>{i['termino']}</td><td>{i['obs']}</td></tr>"
        h += f"<br><h2>ANEXO 1: CALENDARIO</h2><table><tr><th class='th-head'>ACTIVIDAD</th><th class='th-head'>INICIO</th><th class='th-head'>TERMINO</th><th class='th-head'>OBSERVACIÓN</th></tr>{cr}</table><br><hr><p align='center'>FIN DOCUMENTO</p></body>"
        self.editor.setHtml(h)

    def save_progress(self):
        self.controller.current_session["data"]["html_editado"] = self.editor.toHtml()
        self.controller.save_session_data(self.controller.current_session["data"])
        QMessageBox.information(self, "Guardado", "Progreso guardado.")
    def export_doc(self):
        fp, _ = QFileDialog.getSaveFileName(self, "Exportar", "Licitacion.docx", "Word (*.docx)")
        if fp: 
            if self.controller.generate_docx(fp): QMessageBox.information(self, "Éxito", f"Guardado en:\n{fp}")
    def go_back(self): self.controller.cambiar_vista("form")