import re
from datetime import datetime
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QTextEdit, QPushButton, QFrame, 
                               QComboBox, QScrollArea, QCheckBox, QStackedWidget,
                               QGridLayout, QMessageBox, QFileDialog, QSizePolicy)
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QColor, QFont, QCursor, QIntValidator
from src.data.base_texts import TEXTOS_LEGALES

class FormView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        self.EMPRESAS_DATA = {
            "Fundación de Salud Trabajadores Banco Estado de Chile": {
                "rut": "71.235.700-2", "direccion": "Profesora Amanda Labarca N°70, piso 5",
                "comuna": "Santiago", "region": "Metropolitana", "organismo": "Isapre Fundación Banco Estado"
            },
            "Fundación Asistencial Trabajadores BancoEstado de Chile": {
                "rut": "71.980.000-9", "direccion": "Profesora Amanda Labarca N°70",
                "comuna": "Santiago", "region": "Metropolitana", "organismo": "Fundación Asistencial"
            },
            "Centro Médico y Dental Fundación": {
                "rut": "76.123.456-7", "direccion": "Profesora Amanda Labarca N°70",
                "comuna": "Santiago", "region": "Metropolitana", "organismo": "CMDF"
            }
        }

        self.inputs = {}
        self.checkboxes = {}
        self.dynamic_inputs = [] 
        
        self.SECTIONS_LIST = [
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

        self.setStyleSheet("""
            QWidget { background-color: #0f172a; color: #f1f5f9; font-family: 'Segoe UI', sans-serif; }
            QLabel.SectionTitle { color: #3b82f6; font-size: 16px; font-weight: 700; margin-top: 15px; margin-bottom: 5px; border-bottom: 2px solid #1e293b; padding-bottom: 5px; }
            QLabel.SubSectionTitle { color: #2dd4bf; font-size: 14px; font-weight: 700; margin-top: 0px; margin-bottom: 2px; }
            QLabel.PageTitle { color: white; font-size: 24px; font-weight: 800; margin-bottom: 15px; }
            QLabel { color: #94a3b8; font-size: 13px; font-weight: 600; margin-bottom: 2px; background: transparent; border: none; }
            QLineEdit, QTextEdit, QComboBox { background-color: #1e293b; border: 1px solid #334155; border-radius: 6px; padding: 10px 12px; font-size: 14px; color: white; }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus { border: 1px solid #3b82f6; background-color: #26334a; }
            QLineEdit:read-only { background-color: #1e293b; color: #94a3b8; border: 1px solid #334155; }
            QCheckBox { spacing: 10px; color: #cbd5e1; font-size: 14px; margin-bottom: 8px; }
            QCheckBox::indicator { width: 20px; height: 20px; border-radius: 4px; border: 1px solid #475569; background: #1e293b; }
            QCheckBox::indicator:checked { background: #3b82f6; border-color: #3b82f6; }
            QPushButton.NavButton { text-align: left; padding: 12px 15px; color: #94a3b8; border: none; font-size: 14px; font-weight: 600; background: transparent; border-radius: 6px; }
            QPushButton.NavButton:checked { background-color: #1e293b; color: #3b82f6; }
            QPushButton.NavButton:hover { background-color: #1e293b; color: white; }
            QPushButton.BtnDelete { background-color: #ef4444; color: white; border-radius: 4px; font-weight: bold; border: none; }
            QPushButton.BtnDelete:hover { background-color: #dc2626; }
            QPushButton.BtnAdd { background-color: transparent; color: #3b82f6; border: 1px dashed #3b82f6; border-radius: 6px; padding: 8px; font-weight: bold; }
            QPushButton.BtnAdd:hover { background-color: #1e293b; }
        """)

        main_layout = QHBoxLayout(self); main_layout.setContentsMargins(0,0,0,0); main_layout.setSpacing(0)

        sidebar = QFrame(); sidebar.setFixedWidth(260); sidebar.setStyleSheet("background-color: #0f172a; border-right: 1px solid #1e293b;")
        sl = QVBoxLayout(sidebar); sl.setAlignment(Qt.AlignTop); sl.setContentsMargins(15, 30, 15, 20); sl.setSpacing(10)
        sl.addWidget(QLabel("CONFIGURACIÓN", styleSheet="color: white; font-size: 18px; font-weight: 800; padding-left: 10px; margin-bottom: 20px;"))
        
        self.btn_t1 = self.crear_nav("1. Datos Generales", lambda: self.cambiar_tab(0))
        self.btn_t2 = self.crear_nav("2. Estructura Bases", lambda: self.cambiar_tab(1)) 
        sl.addWidget(self.btn_t1); sl.addWidget(self.btn_t2); sl.addStretch()

        self.btn_gen_word = QPushButton("📄 Generar Word")
        self.btn_gen_word.setCursor(Qt.PointingHandCursor); self.btn_gen_word.setFixedHeight(45)
        self.btn_gen_word.setStyleSheet("background-color: #475569; color: #94a3b8; border-radius: 6px; font-weight: bold; border:none;")
        self.btn_gen_word.setEnabled(False) 
        self.btn_gen_word.clicked.connect(self.export_word)
        sl.addWidget(self.btn_gen_word); sl.addSpacing(10)

        self.btn_save = QPushButton("Guardar Progreso")
        self.btn_save.setCursor(Qt.PointingHandCursor); self.btn_save.setFixedHeight(45)
        self.btn_save.setStyleSheet("background-color: #10b981; color: white; border-radius: 6px; font-weight: bold; border:none;")
        self.btn_save.clicked.connect(lambda: self.save_only(show_msg=True))
        sl.addWidget(self.btn_save)

        btn_next = QPushButton("Ir a Archivos  ➜")
        btn_next.setCursor(Qt.PointingHandCursor); btn_next.setFixedHeight(45)
        btn_next.setStyleSheet("background-color: #3b82f6; color: white; border-radius: 6px; font-weight: bold; border:none; margin-top: 10px;")
        btn_next.clicked.connect(self.go_next_view)
        sl.addWidget(btn_next)

        btn_back = QPushButton("❮ Volver"); btn_back.setCursor(Qt.PointingHandCursor)
        btn_back.setStyleSheet("color: #64748b; border: none; margin: 20px; font-weight: bold; background: transparent;")
        btn_back.clicked.connect(self.go_back)
        sl.addWidget(btn_back)

        content = QWidget(); cl = QVBoxLayout(content); cl.setContentsMargins(0,0,0,0)
        self.stack = QStackedWidget(); cl.addWidget(self.stack)
        self.tab1 = QWidget(); self.build_tab_1(); self.stack.addWidget(self.tab1)
        self.tab2 = QWidget(); self.build_tab_structure(); self.stack.addWidget(self.tab2)
        
        main_layout.addWidget(sidebar); main_layout.addWidget(content)
        
        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(lambda: self.save_only(show_msg=False))
        self.autosave_timer.start(60000)
        self.load_existing_data(); self.cambiar_tab(0)

    def crear_nav(self, t, c):
        b=QPushButton(t); b.setProperty("class", "NavButton"); b.setCheckable(True)
        b.setCursor(Qt.PointingHandCursor); b.clicked.connect(c); return b

    def cambiar_tab(self, i): 
        self.stack.setCurrentIndex(i)
        self.btn_t1.setChecked(i==0); self.btn_t2.setChecked(i==1)
        
    def create_label(self, text, css_class=None, style_sheet=None):
        l = QLabel(text)
        if css_class: l.setProperty("class", css_class)
        if style_sheet: l.setStyleSheet(style_sheet)
        return l

    def build_tab_1(self):
        l=QVBoxLayout(self.tab1); l.setContentsMargins(0,0,0,0)
        s=QScrollArea(); s.setWidgetResizable(True)
        c=QWidget(); v=QVBoxLayout(c); v.setContentsMargins(60,30,60,40); v.setSpacing(20); v.setAlignment(Qt.AlignTop)
        s.setWidget(c); l.addWidget(s)
        
        # Estilo amarillo para instrucciones
        YELLOW_INSTR_STYLE = "color: #fbbf24; font-size: 13px; font-weight: 500; font-style: italic; margin-bottom: 5px;"

        # --- SECCIÓN 1: CARACTERÍSTICAS GENERALES ---
        v.addWidget(self.create_label("Características", css_class="PageTitle"))
        v.addWidget(self.create_label("Información General y Empresa", css_class="SectionTitle"))
        g1=QGridLayout(); g1.setVerticalSpacing(15); g1.setHorizontalSpacing(30)
        self.add_field(g1,0,0,"Seleccione Razón Social","razon_social",2,is_combo=True)
        
        self.add_field(g1,1,0,"RUT Empresa","rut_empresa", read_only=True)
        self.add_field(g1,1,1,"Dirección Comercial","direccion", read_only=True)
        self.add_field(g1,2,0,"Comuna","comuna", read_only=True)
        self.add_field(g1,2,1,"Región","region", read_only=True)
        v.addLayout(g1)

        # --- SECCIÓN 2: DATOS LICITACIÓN ---
        v.addWidget(self.create_label("Datos de la Licitación", css_class="SectionTitle"))
        g2=QGridLayout(); g2.setVerticalSpacing(15); g2.setHorizontalSpacing(30)
        self.add_field(g2,0,0,"Nombre de la Adquisición","nombre_adquisicion",2)
        g2.addWidget(QLabel("Descripción Detallada"),1,0,1,2); t=QTextEdit(); t.setFixedHeight(90); self.inputs["descripcion"]=t; g2.addWidget(t,2,0,1,2)
        db_id = self.controller.current_session.get("licitacion_id", 0)
        year = datetime.now().year; db_id = db_id if db_id else self.controller.db.get_next_id()
        self.add_field(g2,3,0,"Folio Interno","folio",read_only=True,val=f"LIC-{year}-{db_id:03d}")
        self.add_field(g2,3,1,"Empresa","organismo",read_only=True)
        self.add_field(g2,4,0,"Duración del Contrato","duracion_contrato",val="12 meses")
        self.add_field(g2,4,1,"Tipo Licitación","tipo_licitacion",val="Licitación Privada")
        self.add_field(g2,5,0,"Moneda","moneda",val="Pesos Chilenos (CLP)", span=2)
        v.addLayout(g2)

        # --- SECCIÓN 3: VALIDEZ ---
        v.addWidget(self.create_label("Validez de la Propuesta", css_class="SectionTitle"))
        v.addWidget(self.create_label("Aquí se indica en <b>días</b> la validez de las ofertas técnicas y económicas", 
                                      style_sheet=YELLOW_INSTR_STYLE))
        g_val = QGridLayout(); g_val.setVerticalSpacing(15); g_val.setHorizontalSpacing(30)
        self.add_field(g_val, 0, 0, "Cantidad de Días", "validez_propuesta", val="30 días")
        v.addLayout(g_val)

        # --- 4. CONSULTAS, ACLARACIONES Y MODIFICACIONES ---
        v.addWidget(self.create_label("CONSULTAS, ACLARACIONES Y MODIFICACIONES", css_class="SectionTitle"))
        v.addWidget(self.create_label("Ingrese el correo electronico de la persona encargada para responder consultas o aclaraciones de las bases", 
                                      style_sheet=YELLOW_INSTR_STYLE))
        g_consultas = QGridLayout(); g_consultas.setVerticalSpacing(15); g_consultas.setHorizontalSpacing(30)
        self.add_field(g_consultas, 0, 0, "Correo Electrónico Encargado", "correo_electronico", span=2)
        v.addLayout(g_consultas)

        # --- 5. ENTREGA DE LAS PROPUESTAS ---
        v.addWidget(self.create_label("ENTREGA DE LAS PROPUESTAS", css_class="SectionTitle"))
        
        # Bloque 1: Encargado/a
        v.addWidget(self.create_label("Ingrese quien será el o la encargado/a de recibir la propuesta", 
                                      style_sheet=YELLOW_INSTR_STYLE))
        g_ent_1 = QGridLayout(); g_ent_1.setVerticalSpacing(15); g_ent_1.setHorizontalSpacing(30)
        self.add_field(g_ent_1, 0, 0, "Encargado/a", "encargado_propuesta", span=2)
        v.addLayout(g_ent_1)
        
        # Bloque 2: Hora
        v.addWidget(self.create_label("Ingrese la hora de la entrega de la propuesta", 
                                      style_sheet=YELLOW_INSTR_STYLE + "margin-top: 10px;"))
        g_ent_2 = QGridLayout(); g_ent_2.setVerticalSpacing(15); g_ent_2.setHorizontalSpacing(30)
        self.add_field(g_ent_2, 0, 0, "Hora de entrega ", "hora_entrega", span=2)
        v.addLayout(g_ent_2)

        # --- 6. COMISIÓN DE EVALUACIÓN ---
        v.addWidget(self.create_label("COMISIÓN DE EVALUACIÓN DE LAS OFERTAS", css_class="SectionTitle"))
        v.addWidget(self.create_label("Ingrese quienes participaran en la comision de evaluacion", 
                                      style_sheet=YELLOW_INSTR_STYLE))
        g_comision = QGridLayout(); g_comision.setVerticalSpacing(15); g_comision.setHorizontalSpacing(30)
        self.add_multiline_field(g_comision, 0, 0, "Comisión de Evaluación", "comision_evaluacion")
        v.addLayout(g_comision)
        
        # --- SECCIÓN: GARANTÍAS ---
        v.addWidget(self.create_label("Garantías", css_class="SectionTitle"))
        sl=QVBoxLayout(); sl.setSpacing(5); sl.setContentsMargins(0,0,0,0)
        sl.addWidget(self.create_label("Seriedad de la Oferta", css_class="SubSectionTitle"))
        gs=QGridLayout(); gs.setHorizontalSpacing(30); gs.setVerticalSpacing(10)
        self.add_field(gs,0,0,"Monto ($)","monto_seriedad")
        self.add_multiline_field(gs,0,1,"Fecha de Vencimiento","vencimiento_seriedad","30 días corridos posteriores a la fecha de presentación de la propuesta.")
        sl.addLayout(gs); sl.addSpacing(10)
        sl.addWidget(self.create_label("Fiel Cumplimiento", css_class="SubSectionTitle"))
        gf=QGridLayout(); gf.setHorizontalSpacing(30); gf.setVerticalSpacing(10)
        self.add_field(gf,0,0,"Monto ($)","monto_cumplimiento")
        self.add_multiline_field(gf,0,1,"Fecha de Vencimiento","vencimiento_cumplimiento","3 meses desde la adjudicación")
        sl.addLayout(gf); v.addLayout(sl)
        self.inputs["monto_seriedad"].editingFinished.connect(lambda: self.fmt_thousands(self.inputs["monto_seriedad"]))
        self.inputs["monto_cumplimiento"].editingFinished.connect(lambda: self.fmt_thousands(self.inputs["monto_cumplimiento"]))
        
        # --- SECCIÓN: EVALUACIÓN Y ADJUDICACIÓN ---
        v.addWidget(self.create_label("Evaluación y Adjudicación de Ofertas", css_class="SectionTitle"))
        v.addWidget(self.create_label("⚠️ La suma de todos los porcentajes debe ser exactamente 100%", style_sheet=YELLOW_INSTR_STYLE))
        self.eval_container=QWidget(); self.eval_layout=QVBoxLayout(self.eval_container); self.eval_layout.setContentsMargins(0,5,0,0); self.eval_layout.setSpacing(10)
        hf=QHBoxLayout(); hf.setSpacing(30)
        
        # Campos de porcentajes (Actualizado con Huella de Carbono)
        self.add_field_vbox(hf, "Oferta Económica (%)", "eval_economica", is_pct=True)
        self.add_field_vbox(hf, "Oferta Técnica (%)", "eval_tecnica", is_pct=True)
        self.add_field_vbox(hf, "Huella de Carbono (%)", "hue_carbono", is_pct=True) # NUEVO CAMPO
        self.add_field_vbox(hf, "Antecedentes Legales (%)", "eval_experiencia", is_pct=True)
        
        self.eval_layout.addLayout(hf)
        self.dynamic_criteria_layout=QVBoxLayout(); self.dynamic_criteria_layout.setContentsMargins(0,0,0,0); self.dynamic_criteria_layout.setSpacing(10)
        self.eval_layout.addLayout(self.dynamic_criteria_layout)
        ba=QPushButton("+ Agregar Criterio Adicional"); ba.setProperty("class", "BtnAdd"); ba.setCursor(Qt.PointingHandCursor); ba.clicked.connect(self.add_dynamic_criteria)
        self.eval_layout.addWidget(ba); v.addWidget(self.eval_container); v.addStretch()

    def build_tab_structure(self):
        l=QVBoxLayout(self.tab2); l.setContentsMargins(0,0,0,0)
        s=QScrollArea(); s.setWidgetResizable(True)
        c=QWidget(); v=QVBoxLayout(c); v.setContentsMargins(60,40,60,40); v.setSpacing(20)
        s.setWidget(c); l.addWidget(s)
        v.addWidget(self.create_label("Estructura del Documento", css_class="PageTitle"))
        v.addWidget(self.create_label("Todos estos items deben ir en la licitación pero puedes marcar y desmarcar si no lo necesitas en tu licitación.", style_sheet="color: #94a3b8; font-size: 14px; margin-bottom: 20px;"))
        for item in self.SECTIONS_LIST:
            k = "check_" + item.lower().replace(" ","_").replace(",","").replace(".","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("/","_")
            chk=QCheckBox(item); chk.setChecked(True); self.checkboxes[k]=chk; v.addWidget(chk)
        v.addStretch()

    def add_field_vbox(self, pl, l, k, is_pct=False):
        cnt=QWidget(); v=QVBoxLayout(cnt); v.setContentsMargins(0,0,0,0); v.setSpacing(5); v.addWidget(QLabel(l))
        w=QLineEdit(); w.setFixedHeight(45); self.inputs[k]=w
        if is_pct: w.setValidator(QIntValidator(0, 100))
        v.addWidget(w); pl.addWidget(cnt)

    def add_dynamic_criteria(self, n="", p=""):
        if isinstance(n, bool): n=""
        if isinstance(p, bool): p=""
        r=QWidget(); rl=QHBoxLayout(r); rl.setContentsMargins(0,0,0,0); rl.setSpacing(30)
        c1=QWidget(); v1=QVBoxLayout(c1); v1.addWidget(QLabel("Criterio")); i1=QLineEdit(n); i1.setFixedHeight(45); v1.addWidget(i1)
        c2=QWidget(); v2=QVBoxLayout(c2); v2.addWidget(QLabel("%")); i2=QLineEdit(p); i2.setFixedHeight(45)
        i2.setValidator(QIntValidator(0, 100)); v2.addWidget(i2)
        b=QPushButton("✕"); b.setFixedSize(45,45); b.setProperty("class", "BtnDelete"); b.clicked.connect(lambda: self.remove_dynamic_criteria(r,i1,i2))
        rl.addWidget(c1,2); rl.addWidget(c2,1); rl.addWidget(b)
        self.dynamic_criteria_layout.addWidget(r); self.dynamic_inputs.append((i1,i2,r))
    
    def remove_dynamic_criteria(self, r, i1, i2):
        self.dynamic_criteria_layout.removeWidget(r); r.deleteLater()
        if (i1,i2,r) in self.dynamic_inputs: self.dynamic_inputs.remove((i1,i2,r))
        
    def add_field(self, g, r, c, l, k, span=1, read_only=False, val="", is_combo=False):
        cnt=QWidget(); v=QVBoxLayout(cnt); v.setContentsMargins(0,0,0,0); v.setSpacing(5)
        lbl = QLabel(l); lbl.setWordWrap(True); v.addWidget(lbl)
        if is_combo: w=QComboBox(); w.addItems([""]+list(self.EMPRESAS_DATA.keys())); w.currentTextChanged.connect(self.autofill_provider_data)
        else: w=QLineEdit(val); w.setReadOnly(read_only)
        w.setFixedHeight(45); self.inputs[k]=w; v.addWidget(w); g.addWidget(cnt, r, c, 1, span)
    
    def add_multiline_field(self, g, r, c, l, k, val=""):
        cnt=QWidget(); v=QVBoxLayout(cnt); v.setContentsMargins(0,0,0,0); v.setSpacing(5)
        lbl = QLabel(l); lbl.setWordWrap(True); v.addWidget(lbl)
        w=QTextEdit(val); w.setFixedHeight(75); self.inputs[k]=w; v.addWidget(w); g.addWidget(cnt, r, c, 1, 1)
    
    def autofill_provider_data(self, t):
        d = self.EMPRESAS_DATA.get(t)
        if d: self.inputs["rut_empresa"].setText(d["rut"]); self.inputs["direccion"].setText(d["direccion"]); self.inputs["comuna"].setText(d["comuna"]); self.inputs["region"].setText(d["region"]); self.inputs["organismo"].setText(d.get("organismo",""))
    
    def fmt_thousands(self, w): t=w.text().replace(".",""); w.setText("{:,}".format(int(t)).replace(",", ".") if t.isdigit() else t)

    def validate_percentages(self):
        total = 0
        # AQUI: Se agrega 'hue_carbono' a la validación
        for k in ["eval_economica", "eval_tecnica", "hue_carbono", "eval_experiencia"]:
            try: val = int(self.inputs[k].text().strip())
            except: val = 0
            total += val
        for _, i_pct, _ in self.dynamic_inputs:
            try: val = int(i_pct.text().strip())
            except: val = 0
            total += val
        return True, total

    def _save_internal(self, silent=False):
        _, total = self.validate_percentages()
        if total != 100:
            if not silent: 
                msg = f"La suma de los porcentajes es {total}%.\n"
                if total > 100: msg += "No debe exceder el 100%."
                else: msg += "No puede ser menor al 100%."
                QMessageBox.warning(self, "Error de Validación", msg)
            return False
            
        d = {}
        for k, w in self.inputs.items(): d[k] = w.toPlainText() if isinstance(w, QTextEdit) else (w.currentText() if isinstance(w, QComboBox) else w.text())
        for k, w in self.checkboxes.items(): d[k] = 1 if w.isChecked() else 0
        d["check_bases_tecnicas"] = 1
        dyn, txt = [], ""
        for n, p, _ in self.dynamic_inputs:
            nv, pv = n.text().strip(), p.text().strip()
            if nv: dyn.append({"name":nv, "pct":pv}); txt += f"\n- {nv}: {pv}%"
        d["extra_criteria"] = dyn; d["otros_criterios"] = txt
        
        if not d.get("razon_social") or not d.get("nombre_adquisicion"): 
            if not silent: QMessageBox.warning(self, "Faltan Datos", "Complete Razón Social y Nombre.")
            return False
        self.controller.save_session_data(d)
        return True

    def save_only(self, show_msg=True):
        if self._save_internal(silent=not show_msg): 
            self.btn_gen_word.setEnabled(True)
            self.btn_gen_word.setStyleSheet("background-color: #2563eb; color: white; border-radius: 6px; font-weight: bold; border:none;")
            if show_msg: QMessageBox.information(self, "Guardado", "Datos guardados.")

    def export_word(self):
        if not self._save_internal(): return
        path, _ = QFileDialog.getSaveFileName(self, "Guardar Licitación", "Licitacion.docx", "Word Files (*.docx)")
        if path: self.controller.generate_docx(path)

    def go_next_view(self): 
        if self._save_internal(): self.controller.cambiar_vista("files")

    def go_back(self): self.controller.cambiar_vista("welcome")
    
    def load_existing_data(self):
        d = self.controller.current_session.get("data", {})
        for k, v in d.items():
            if k in self.inputs:
                w = self.inputs[k]
                if isinstance(w, QComboBox): w.setCurrentText(str(v))
                elif isinstance(w, QTextEdit): w.setPlainText(str(v))
                else: w.setText(str(v))
        for k, v in d.items():
            if k in self.checkboxes: self.checkboxes[k].setChecked(bool(v))
        while self.dynamic_inputs: i1, i2, r = self.dynamic_inputs[0]; self.remove_dynamic_criteria(r, i1, i2)
        for item in d.get("extra_criteria", []): self.add_dynamic_criteria(item.get("name", ""), item.get("pct", ""))