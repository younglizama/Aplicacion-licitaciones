import re
from datetime import datetime
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QTextEdit, QPushButton, QFrame, 
                               QComboBox, QScrollArea, QCheckBox, QStackedWidget,
                               QGridLayout, QMessageBox, QDialog, QTextBrowser)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QFont, QCursor

# Importamos los textos para que la vista previa sea real
from src.data.base_texts import TEXTOS_LEGALES

# --- VENTANA DE VISTA PREVIA ---
class DocumentPreviewDialog(QDialog):
    def __init__(self, html_content, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Vista Previa del Documento")
        self.setFixedSize(1000, 900) 
        self.setStyleSheet("background-color: #0f172a;")
        
        layout = QVBoxLayout(self)
        
        lbl_info = QLabel("Vista Previa (Idéntica al Editor)")
        lbl_info.setStyleSheet("color: white; font-weight: bold; font-size: 16px; margin-bottom: 5px;")
        layout.addWidget(lbl_info)
        
        self.viewer = QTextBrowser()
        self.viewer.setHtml(html_content)
        self.viewer.setStyleSheet("""
            QTextBrowser {
                background-color: white;
                color: black;
                font-family: 'Times New Roman', serif;
                font-size: 14px;
                padding: 50px;
                border: 1px solid #cbd5e1;
            }
        """)
        layout.addWidget(self.viewer)
        
        btn_close = QPushButton("Cerrar")
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.setFixedHeight(40)
        btn_close.setStyleSheet("""
            QPushButton { background-color: #3b82f6; color: white; border-radius: 6px; font-weight: bold; }
            QPushButton:hover { background-color: #2563eb; }
        """)
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)

class FormView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        self.EMPRESAS_DATA = {
            "Fundación de Salud Trabajadores Banco Estado de Chile": {
                "rut": "71.235.700-2", "direccion": "Profesora Amanda Labarca N°70, piso 5",
                "comuna": "Santiago", "region": "Metropolitana", "organismo": "Isapre Fundación Banco Estado"
            },
            "Servicios Integrales Beta Ltda": {
                "rut": "77.222.222-K", "direccion": "Av. Ejemplo 123",
                "comuna": "Valparaíso", "region": "Valparaíso", "organismo": "Servicios Beta"
            }
        }

        self.inputs = {}
        self.checkboxes = {}
        self.dynamic_inputs = [] 
        self.calendar_rows = []  

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

        # Estilos CSS
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

        # LAYOUT
        main_layout = QHBoxLayout(self); main_layout.setContentsMargins(0,0,0,0); main_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame(); sidebar.setFixedWidth(260); sidebar.setStyleSheet("background-color: #0f172a; border-right: 1px solid #1e293b;")
        sl = QVBoxLayout(sidebar); sl.setAlignment(Qt.AlignTop); sl.setContentsMargins(15, 30, 15, 20); sl.setSpacing(10)
        sl.addWidget(QLabel("CONFIGURACIÓN", styleSheet="color: white; font-size: 18px; font-weight: 800; padding-left: 10px; margin-bottom: 20px;"))
        
        # --- TABS ---
        self.btn_t1 = self.crear_nav("1. Características Generales", lambda: self.cambiar_tab(0))
        self.btn_t2 = self.crear_nav("2. Estructura Bases", lambda: self.cambiar_tab(1)) 
        self.btn_t3 = self.crear_nav("3. Calendario y Anexos", lambda: self.cambiar_tab(2))    
        
        sl.addWidget(self.btn_t1); sl.addWidget(self.btn_t2); sl.addWidget(self.btn_t3); sl.addStretch()

        self.btn_save = QPushButton("Guardar Progreso")
        self.btn_save.setCursor(Qt.PointingHandCursor); self.btn_save.setFixedHeight(45)
        self.btn_save.setStyleSheet("background-color: #10b981; color: white; border-radius: 6px; font-weight: bold; border:none;")
        self.btn_save.clicked.connect(self.save_only)
        sl.addWidget(self.btn_save)

        # Botón Vista Previa
        self.btn_preview = QPushButton("👁️ Vista Previa")
        self.btn_preview.setCursor(Qt.PointingHandCursor); self.btn_preview.setFixedHeight(45)
        self.btn_preview.setStyleSheet("background-color: #475569; color: #94a3b8; border-radius: 6px; font-weight: bold; border:none;")
        self.btn_preview.setEnabled(False)
        self.btn_preview.clicked.connect(self.show_preview_data)
        sl.addWidget(self.btn_preview)

        btn_next = QPushButton("Ir al Editor  ➜")
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
        self.tab3 = QWidget(); self.build_tab_calendar(); self.stack.addWidget(self.tab3)
        
        main_layout.addWidget(sidebar); main_layout.addWidget(content)
        self.load_existing_data(); self.cambiar_tab(0)

    def crear_nav(self, t, c):
        b=QPushButton(t); b.setProperty("class", "NavButton"); b.setCheckable(True)
        b.setCursor(Qt.PointingHandCursor); b.clicked.connect(c); return b
    
    def cambiar_tab(self, i): 
        self.stack.setCurrentIndex(i)
        self.btn_t1.setChecked(i==0); self.btn_t2.setChecked(i==1); self.btn_t3.setChecked(i==2)

    def create_label(self, text, css_class=None, style_sheet=None):
        l = QLabel(text)
        if css_class: l.setProperty("class", css_class)
        if style_sheet: l.setStyleSheet(style_sheet)
        return l

    # --- TAB 1: DATOS ---
    def build_tab_1(self):
        l=QVBoxLayout(self.tab1); l.setContentsMargins(0,0,0,0)
        s=QScrollArea(); s.setWidgetResizable(True)
        c=QWidget(); v=QVBoxLayout(c); v.setContentsMargins(60,30,60,40); v.setSpacing(20); v.setAlignment(Qt.AlignTop)
        s.setWidget(c); l.addWidget(s)

        v.addWidget(self.create_label("Características", css_class="PageTitle"))
        
        v.addWidget(self.create_label("Información General y Empresa", css_class="SectionTitle"))
        g1=QGridLayout(); g1.setVerticalSpacing(15); g1.setHorizontalSpacing(30)
        self.add_field(g1,0,0,"Seleccione Razón Social","razon_social",2,is_combo=True)
        self.add_field(g1,1,0,"RUT Empresa","rut_empresa",read_only=True)
        self.add_field(g1,1,1,"Dirección Comercial","direccion",read_only=True)
        self.add_field(g1,2,0,"Comuna","comuna",read_only=True)
        self.add_field(g1,2,1,"Región","region",read_only=True)
        v.addLayout(g1)

        v.addWidget(self.create_label("Datos de la Licitación", css_class="SectionTitle"))
        g2=QGridLayout(); g2.setVerticalSpacing(15); g2.setHorizontalSpacing(30)
        self.add_field(g2,0,0,"Nombre de la Adquisición","nombre_adquisicion",2)
        g2.addWidget(QLabel("Descripción Detallada"),1,0,1,2); t=QTextEdit(); t.setFixedHeight(90); self.inputs["descripcion"]=t; g2.addWidget(t,2,0,1,2)
        db_id = self.controller.current_session.get("licitacion_id", 0)
        year = datetime.now().year; db_id = db_id if db_id else self.controller.db.get_next_id()
        self.add_field(g2,3,0,"Folio Interno","folio",read_only=True,val=f"LIC-{year}-{db_id:03d}")
        self.add_field(g2,3,1,"Empresa","organismo",read_only=True)
        self.add_field(g2,4,0,"Duración del Contrato","duracion_contrato",val="30 Días")
        self.add_field(g2,4,1,"Tipo Licitación","tipo_licitacion",val="Licitación Privada")
        self.add_field(g2,5,0,"Moneda","moneda",val="Pesos Chilenos (CLP)", span=2)
        v.addLayout(g2)

        v.addWidget(self.create_label("Garantías", css_class="SectionTitle"))
        sl=QVBoxLayout(); sl.setSpacing(5); sl.setContentsMargins(0,0,0,0)
        sl.addWidget(self.create_label("Seriedad de la Oferta", css_class="SubSectionTitle"))
        gs=QGridLayout(); gs.setHorizontalSpacing(30); gs.setVerticalSpacing(10)
        self.add_field(gs,0,0,"Monto ($)","monto_seriedad")
        self.add_multiline_field(gs,0,1,"Fecha de Vencimiento","vencimiento_seriedad","30 días corridos posteriores...")
        sl.addLayout(gs); sl.addSpacing(10)
        sl.addWidget(self.create_label("Fiel Cumplimiento", css_class="SubSectionTitle"))
        gf=QGridLayout(); gf.setHorizontalSpacing(30); gf.setVerticalSpacing(10)
        self.add_field(gf,0,0,"Monto ($)","monto_cumplimiento")
        self.add_multiline_field(gf,0,1,"Fecha de Vencimiento","vencimiento_cumplimiento","3 meses desde la adjudicación")
        sl.addLayout(gf); v.addLayout(sl)
        self.inputs["monto_seriedad"].editingFinished.connect(lambda: self.fmt_thousands(self.inputs["monto_seriedad"]))
        self.inputs["monto_cumplimiento"].editingFinished.connect(lambda: self.fmt_thousands(self.inputs["monto_cumplimiento"]))

        # --- EVALUACIÓN (RESTAURO EL DISEÑO ORIGINAL) ---
        v.addWidget(self.create_label("Evaluación y Adjudicación de Ofertas", css_class="SectionTitle"))
        v.addWidget(self.create_label("⚠️ La suma de todos los porcentajes no debe exceder el 100%", style_sheet="color: #fbbf24; font-size: 13px; font-weight: 500; font-style: italic; margin-bottom: 5px;"))
        
        self.eval_container=QWidget(); 
        self.eval_layout=QVBoxLayout(self.eval_container); 
        self.eval_layout.setContentsMargins(0,5,0,0); 
        self.eval_layout.setSpacing(10)
        
        # Inputs horizontales
        hf=QHBoxLayout(); hf.setSpacing(30)
        self.add_field_vbox(hf,"Oferta Económica (%)","eval_economica")
        self.add_field_vbox(hf,"Oferta Técnica (%)","eval_tecnica")
        self.add_field_vbox(hf,"Antecedentes Legales (%)","eval_experiencia")
        self.eval_layout.addLayout(hf)
        
        self.dynamic_criteria_layout=QVBoxLayout(); self.dynamic_criteria_layout.setContentsMargins(0,0,0,0); self.dynamic_criteria_layout.setSpacing(10)
        self.eval_layout.addLayout(self.dynamic_criteria_layout)
        
        ba=QPushButton("+ Agregar Criterio Adicional"); ba.setProperty("class", "BtnAdd"); ba.setCursor(Qt.PointingHandCursor); ba.clicked.connect(self.add_dynamic_criteria)
        self.eval_layout.addWidget(ba); v.addWidget(self.eval_container); v.addStretch()

    # --- TAB 2: ESTRUCTURA ---
    def build_tab_structure(self):
        l=QVBoxLayout(self.tab2); l.setContentsMargins(0,0,0,0)
        s=QScrollArea(); s.setWidgetResizable(True)
        c=QWidget(); v=QVBoxLayout(c); v.setContentsMargins(60,40,60,40); v.setSpacing(20)
        s.setWidget(c); l.addWidget(s)
        v.addWidget(self.create_label("Estructura del Documento", css_class="PageTitle"))
        v.addWidget(self.create_label("Seleccione los apartados opcionales:", style_sheet="color: #94a3b8; font-size: 14px; margin-bottom: 20px;"))
        for item in self.SECTIONS_LIST:
            k = "check_" + item.lower().replace(" ","_").replace(",","").replace(".","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("/","_")
            chk=QCheckBox(item); chk.setChecked(True); self.checkboxes[k]=chk; v.addWidget(chk)
        v.addStretch()

    # --- TAB 3: CALENDARIO ---
    def build_tab_calendar(self):
        l=QVBoxLayout(self.tab3); l.setContentsMargins(0,0,0,0)
        s=QScrollArea(); s.setWidgetResizable(True)
        c=QWidget(); v=QVBoxLayout(c); v.setContentsMargins(60,30,60,40); v.setSpacing(20); v.setAlignment(Qt.AlignTop)
        s.setWidget(c); l.addWidget(s)

        v.addWidget(self.create_label("Anexo N°1: Calendario", css_class="PageTitle"))
        v.addWidget(self.create_label("Defina las actividades clave del proceso (Actividad, Inicio, Término, Obs).", style_sheet="color: #94a3b8; margin-bottom: 20px;"))

        h = QWidget(); hl = QHBoxLayout(h); hl.setContentsMargins(0,0,0,0); hl.setSpacing(10)
        hl.addWidget(QLabel("ACTIVIDAD"), 3); hl.addWidget(QLabel("F. INICIO"), 1); hl.addWidget(QLabel("F. TÉRMINO"), 1); hl.addWidget(QLabel("OBSERVACIÓN"), 2); hl.addWidget(QLabel(""), 0) 
        v.addWidget(h)

        self.calendar_layout = QVBoxLayout(); self.calendar_layout.setSpacing(10)
        v.addLayout(self.calendar_layout)

        btn_add = QPushButton("+ Agregar Fila"); btn_add.setProperty("class", "BtnAdd"); btn_add.setCursor(Qt.PointingHandCursor)
        btn_add.clicked.connect(self.add_calendar_row)
        v.addWidget(btn_add); v.addStretch()

    def add_calendar_row(self, act="", ini="", fin="", obs=""):
        if isinstance(act, bool): act=""
        if isinstance(ini, bool): ini=""
        row_widget = QWidget(); rl = QHBoxLayout(row_widget); rl.setContentsMargins(0,0,0,0); rl.setSpacing(10)
        i_act = QLineEdit(act); i_act.setPlaceholderText("Ej: Publicación"); i_act.setFixedHeight(40)
        i_ini = QLineEdit(ini); i_ini.setPlaceholderText("Ej: 15-10"); i_ini.setFixedHeight(40)
        i_fin = QLineEdit(fin); i_fin.setPlaceholderText("Ej: 20-10"); i_fin.setFixedHeight(40)
        i_obs = QLineEdit(obs); i_obs.setPlaceholderText("Opcional"); i_obs.setFixedHeight(40)
        b_del = QPushButton("✕"); b_del.setFixedSize(40,40); b_del.setProperty("class", "BtnDelete"); b_del.setCursor(Qt.PointingHandCursor)
        rl.addWidget(i_act, 3); rl.addWidget(i_ini, 1); rl.addWidget(i_fin, 1); rl.addWidget(i_obs, 2); rl.addWidget(b_del)
        self.calendar_layout.addWidget(row_widget)
        entry = {"widget": row_widget, "i_act": i_act, "i_ini": i_ini, "i_fin": i_fin, "i_obs": i_obs}
        self.calendar_rows.append(entry)
        b_del.clicked.connect(lambda: self.remove_calendar_row(entry))

    def remove_calendar_row(self, entry):
        self.calendar_layout.removeWidget(entry["widget"]); entry["widget"].deleteLater()
        if entry in self.calendar_rows: self.calendar_rows.remove(entry)

    # --- HELPERS (AQUÍ ESTABA EL ERROR QUE CORREGÍ: v.addWidget(w)) ---
    def add_field_vbox(self, pl, l, k):
        cnt=QWidget(); v=QVBoxLayout(cnt); v.setContentsMargins(0,0,0,0); v.setSpacing(5); v.addWidget(QLabel(l))
        w=QLineEdit(); w.setFixedHeight(45); self.inputs[k]=w
        v.addWidget(w) # <--- ¡ESTA LÍNEA FALTABA Y AHORA ESTÁ! 
        pl.addWidget(cnt)

    def add_dynamic_criteria(self, n="", p=""):
        if isinstance(n, bool): n=""
        if isinstance(p, bool): p=""
        r=QWidget(); rl=QHBoxLayout(r); rl.setContentsMargins(0,0,0,0); rl.setSpacing(30)
        c1=QWidget(); v1=QVBoxLayout(c1); v1.addWidget(QLabel("Criterio")); i1=QLineEdit(n); i1.setFixedHeight(45); v1.addWidget(i1)
        c2=QWidget(); v2=QVBoxLayout(c2); v2.addWidget(QLabel("%")); i2=QLineEdit(p); i2.setFixedHeight(45); v2.addWidget(i2)
        b=QPushButton("✕"); b.setFixedSize(45,45); b.setProperty("class", "BtnDelete"); b.clicked.connect(lambda: self.remove_dynamic_criteria(r,i1,i2))
        rl.addWidget(c1,2); rl.addWidget(c2,1); rl.addWidget(b)
        self.dynamic_criteria_layout.addWidget(r); self.dynamic_inputs.append((i1,i2,r))
    
    def remove_dynamic_criteria(self, r, i1, i2):
        self.dynamic_criteria_layout.removeWidget(r); r.deleteLater()
        if (i1,i2,r) in self.dynamic_inputs: self.dynamic_inputs.remove((i1,i2,r))
        
    def add_field(self, g, r, c, l, k, span=1, read_only=False, val="", is_combo=False):
        cnt=QWidget(); v=QVBoxLayout(cnt); v.setContentsMargins(0,0,0,0); v.setSpacing(5); v.addWidget(QLabel(l))
        if is_combo: w=QComboBox(); w.addItems([""]+list(self.EMPRESAS_DATA.keys())); w.currentTextChanged.connect(self.autofill_provider_data)
        else: w=QLineEdit(val); w.setReadOnly(read_only)
        w.setFixedHeight(45); self.inputs[k]=w; v.addWidget(w); g.addWidget(cnt, r, c, 1, span)
    
    def add_multiline_field(self, g, r, c, l, k, val=""):
        cnt=QWidget(); v=QVBoxLayout(cnt); v.setContentsMargins(0,0,0,0); v.setSpacing(5); v.addWidget(QLabel(l))
        w=QTextEdit(val); w.setFixedHeight(75); self.inputs[k]=w; v.addWidget(w); g.addWidget(cnt, r, c, 1, 1)
    
    def autofill_provider_data(self, t):
        d = self.EMPRESAS_DATA.get(t)
        if d: self.inputs["rut_empresa"].setText(d["rut"]); self.inputs["direccion"].setText(d["direccion"]); self.inputs["comuna"].setText(d["comuna"]); self.inputs["region"].setText(d["region"]); self.inputs["organismo"].setText(d.get("organismo",""))
    
    def fmt_thousands(self, w): t=w.text().replace(".",""); w.setText("{:,}".format(int(t)).replace(",", ".") if t.isdigit() else t)

    # --- VALIDACIÓN DEL 100% ---
    def validate_percentages(self):
        total = 0
        # Sumar campos fijos
        for k in ["eval_economica", "eval_tecnica", "eval_experiencia"]:
            try: val = int(self.inputs[k].text().strip())
            except: val = 0
            total += val
        
        # Sumar dinámicos
        for _, i_pct, _ in self.dynamic_inputs:
            try: val = int(i_pct.text().strip())
            except: val = 0
            total += val
            
        if total > 100:
            QMessageBox.warning(self, "Error de Validación", f"La suma de los porcentajes es {total}%. No debe exceder el 100%.")
            return False
        return True

    def _save_internal(self):
        # VALIDAR ANTES DE GUARDAR
        if not self.validate_percentages():
            return False

        d = {}
        for k, w in self.inputs.items(): d[k] = w.toPlainText() if isinstance(w, QTextEdit) else (w.currentText() if isinstance(w, QComboBox) else w.text())
        for k, w in self.checkboxes.items(): d[k] = 1 if w.isChecked() else 0
        
        dyn, txt = [], ""
        for n, p, _ in self.dynamic_inputs:
            nv, pv = n.text().strip(), p.text().strip()
            if nv: dyn.append({"name":nv, "pct":pv}); txt += f"\n- {nv}: {pv}%"
        d["extra_criteria"] = dyn; d["otros_criterios"] = txt
        
        cal_data = []
        for entry in self.calendar_rows:
            cal_data.append({
                "actividad": entry["i_act"].text().strip(),
                "inicio": entry["i_ini"].text().strip(),
                "termino": entry["i_fin"].text().strip(),
                "obs": entry["i_obs"].text().strip()
            })
        d["calendario"] = cal_data

        if not d.get("razon_social") or not d.get("nombre_adquisicion"): 
            QMessageBox.warning(self, "Faltan Datos", "Complete Razón Social y Nombre.")
            return False
            
        self.controller.save_session_data(d)
        return True

    def save_only(self):
        if self._save_internal(): 
            self.btn_preview.setEnabled(True)
            self.btn_preview.setStyleSheet("background-color: #8b5cf6; color: white; border-radius: 6px; font-weight: bold; border:none;")
            QMessageBox.information(self, "Guardado", "Datos guardados. Vista Previa habilitada.")

    # --- LÓGICA COMPLETA DE VISTA PREVIA ---
    def show_preview_data(self):
        d = self.controller.current_session.get("data", {})
        
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

        for titulo in self.SECTIONS_LIST:
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
        """
        DocumentPreviewDialog(html, self).exec()

    def go_next_view(self): 
        if self._save_internal(): self.controller.cambiar_vista("editor")
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
        for item in d.get("extra_criteria", []): self.add_dynamic_criteria(item.get("name", ""), item.get("pct", ""))
        
        for entry in self.calendar_rows: self.calendar_layout.removeWidget(entry["widget"]); entry["widget"].deleteLater()
        self.calendar_rows = []
        saved_cal = d.get("calendario", [])
        if not saved_cal:
            default_acts = ["Publicación de Bases", "Consultas", "Respuestas", "Cierre Ofertas", "Adjudicación"]
            for act in default_acts: self.add_calendar_row(act, "", "", "")
        else:
            for item in saved_cal: self.add_calendar_row(item.get("actividad"), item.get("inicio"), item.get("termino"), item.get("obs"))