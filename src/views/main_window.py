import os
import platform
import subprocess
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox
from src.views.view_welcome import WelcomeView
from src.views.view_form import FormView
from src.views.view_files import FilesView
from src.views.view_chat import ChatView
from database.db_manager import DBManager
import config
from src.controllers.doc_generator import DocumentGenerator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Licitaciones - Isapre Fundación")
        self.resize(1300, 850); self.setMinimumSize(1000, 700)
        self.db = DBManager(); self.db.init_db()
        self.current_session = {"licitacion_id": None, "data": {}}
        
        self.central_stack = QStackedWidget(); self.setCentralWidget(self.central_stack)
        
        self.view_welcome = WelcomeView(self)
        self.view_form = FormView(self)
        self.view_files = FilesView(self)
        
        self.central_stack.addWidget(self.view_welcome) 
        self.central_stack.addWidget(self.view_form)    
        self.central_stack.addWidget(self.view_files)   
        
        try: self.chat_helper = ChatView(self)
        except: self.chat_helper = None
        self.cambiar_vista("welcome")

    def cambiar_vista(self, view_name):
        if view_name == "welcome": self.central_stack.setCurrentIndex(0); self._set_chat_visible(False)
        elif view_name == "form": self.central_stack.setCurrentIndex(1); self.view_form.load_existing_data(); self._set_chat_visible(True)
        elif view_name == "files": self.central_stack.setCurrentIndex(2); self.view_files.load_history(); self._set_chat_visible(True)

    def _set_chat_visible(self, visible):
        if self.chat_helper and hasattr(self.chat_helper, 'fab'):
            if visible: self.chat_helper.fab.show(); self.chat_helper.fab.raise_()
            else: self.chat_helper.fab.hide(); self.chat_helper.is_open and self.chat_helper.close_chat()

    def start_new_licitacion(self):
        self.current_session["licitacion_id"] = None; self.current_session["data"] = {}
        self.cambiar_vista("form")

    def save_session_data(self, form_data):
        self.current_session["data"].update(form_data)
        saved_id = self.db.guardar_licitacion(self.current_session["data"], self.current_session["licitacion_id"])
        if not self.current_session["licitacion_id"] and saved_id: self.current_session["licitacion_id"] = saved_id
        return saved_id

    def generate_preview_html(self): return "<html><body>Vista previa no disponible en este modo</body></html>"

    def generate_docx(self, output_path):
        try:
            print(f"🚀 Generando DOCX en: {output_path}")
            context = self.current_session["data"].copy()

            # 1. Variables Simples
            raw_name = str(context.get("nombre_adquisicion", ""))
            context["nombre_adquisicion"] = raw_name 
            context["nombre_adquisicion_titulo"] = raw_name.upper()

            if 'duracion_contrato' in context: context['duración_contrato'] = context['duracion_contrato']

            # 2. Generar Interruptores (True/False)
            KEYS_CHECKBOX = [
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

            for key in KEYS_CHECKBOX:
                # Transforma "OBJETIVOS" -> "check_objetivos" -> "mostrar_objetivos"
                internal_key = "check_" + key.lower().replace(" ","_").replace(",","").replace(".","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("/","_")
                word_var_name = f"mostrar_{internal_key.replace('check_', '')}"
                context[word_var_name] = bool(context.get(internal_key, 0))

            context["mostrar_caracteristicas"] = context.get("mostrar_caracteristicas_de_la_licitacion", False)
            context["mostrar_bases_tecnicas"] = bool(context.get("check_bases_tecnicas", 0))

            # IMPORTANTE: No generamos RichText. Confiamos en que la plantilla tiene las tablas.

            gen = DocumentGenerator(os.path.join(config.TEMPLATE_DIR, "plantilla_base.docx"))
            success, msg = gen.generar_word(context, output_path)
            
            if success:
                if self.current_session["licitacion_id"]: self.db.actualizar_ruta_archivo(self.current_session["licitacion_id"], output_path)
                resp = QMessageBox.question(self, "Éxito", f"Documento generado exitosamente.\n¿Deseas abrirlo ahora?", QMessageBox.Yes | QMessageBox.No)
                if resp == QMessageBox.Yes:
                    try:
                        if platform.system() == 'Windows': os.startfile(output_path)
                        elif platform.system() == 'Darwin': subprocess.call(('open', output_path))
                        else: subprocess.call(('xdg-open', output_path))
                    except: pass
                return True
            else: QMessageBox.warning(self, "Error", msg); return False
        except Exception as e: print(f"Error: {e}"); QMessageBox.critical(self, "Error", str(e)); return False