import os
import re
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox
from docxtpl import RichText 

from src.views.view_welcome import WelcomeView
from src.views.view_form import FormView
from src.views.view_editor import EditorView
from src.views.view_files import FilesView
from src.views.view_chat import ChatView
from database.db_manager import DBManager

import config
from src.controllers.doc_generator import DocumentGenerator
from src.data.base_texts import TEXTOS_LEGALES

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
        self.view_editor = EditorView(self)
        self.view_files = FilesView(self)
        
        self.central_stack.addWidget(self.view_welcome)
        self.central_stack.addWidget(self.view_form)
        self.central_stack.addWidget(self.view_editor)
        self.central_stack.addWidget(self.view_files)
        
        try: self.chat_helper = ChatView(self)
        except: self.chat_helper = None
        self.cambiar_vista("welcome")

    def cambiar_vista(self, view_name):
        if view_name == "welcome": self.central_stack.setCurrentIndex(0); self._set_chat_visible(False)
        elif view_name == "form": self.central_stack.setCurrentIndex(1); self.view_form.load_existing_data(); self._set_chat_visible(True)
        elif view_name == "editor": self.central_stack.setCurrentIndex(2); self.view_editor.load_data_variables(); self._set_chat_visible(True)
        elif view_name == "files": self.central_stack.setCurrentIndex(3); self.view_files.load_history(); self._set_chat_visible(True)

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

    def html_to_richtext(self, html_text):
        if not html_text: return ""
        rt = RichText()
        text = html_text.replace("<br>", "\n").replace("<br/>", "\n").replace("<ul>", "").replace("</ul>", "")
        parts = re.split(r'(<b>.*?</b>|<li>.*?</li>)', text, flags=re.DOTALL)
        for part in parts:
            if not part: continue
            if part.startswith("<b>") and part.endswith("</b>"): rt.add(part[3:-4], bold=True)
            elif part.startswith("<li>") and part.endswith("</li>"): rt.add("\n• " + part[4:-5])
            else: rt.add(part)
        return rt

    def generate_docx(self, output_path):
        try:
            print(f"🚀 Generando DOCX en: {output_path}")
            context = self.current_session["data"].copy()

            if 'duracion_contrato' in context: context['duración_contrato'] = context['duracion_contrato']

            # LISTA ORDENADA EXACTA (Indices)
            ORDERED_KEYS = [
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

            idx = 1
            rt_bloque_admin = RichText() # Variable maestra para bloques de texto

            for key in ORDERED_KEYS:
                checkbox_key = "check_" + key.lower().replace(" ","_").replace(",","").replace(".","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("/","_")
                show_key = f"mostrar_{checkbox_key.replace('check_', '')}"
                
                if not context.get(checkbox_key, 0): 
                    context[key] = ""
                    context[show_key] = False
                    continue
                
                context[show_key] = True

                # --- LÓGICA DE GENERACIÓN ---

                # 1. CARACTERÍSTICAS: Solo título (Tabla en Word)
                if key == "CARACTERÍSTICAS DE LA LICITACIÓN":
                    rt = RichText()
                    rt.add(f"{key}\n", bold=True, size=28) # Tamaño grande (aprox 14pt)
                    context["CARACTERÍSTICAS_DE_LA_LICITACIÓN"] = rt
                    # No incrementamos idx (índice)

                # 2. GARANTÍAS: Solo título numerado (Tabla en Word)
                elif key == "GARANTÍAS":
                    rt = RichText()
                    rt.add(f"{idx}. {key}", bold=True, size=32) # Tamaño más grande (aprox 16pt)
                    context["GARANTÍAS"] = rt
                    idx += 1

                # 3. EVALUACIÓN: Título numerado + Texto generado (Word no tiene tabla fija aqui)
                elif key == "EVALUACIÓN Y ADJUDICACIÓN DE LAS OFERTAS":
                    rt = RichText()
                    rt.add(f"{idx}. {key}\n", bold=True, size=32)
                    rt.add("Ponderación de Criterios:\n", bold=True, size=24)
                    rt.add(f"• Económica: {context.get('eval_economica','0')}%\n", size=24)
                    rt.add(f"• Técnica: {context.get('eval_tecnica','0')}%\n", size=24)
                    rt.add(f"• Experiencia: {context.get('eval_experiencia','0')}%\n", size=24)
                    if context.get('extra_criteria'):
                         for c in context.get('extra_criteria'): 
                             rt.add(f"• {c.get('name')}: {c.get('pct')}%\n", size=24)
                    rt.add("\nAdjudicación al mayor puntaje.", size=24)
                    context["EVALUACIÓN_Y_ADJUDICACIÓN_DE_LAS_OFERTAS"] = rt
                    idx += 1

                # 4. RESTO DE SECCIONES (Objetivos, Plazos...): Van al bloque común
                else:
                    text_template = TEXTOS_LEGALES.get(key, "")
                    try: final_text = text_template.format(**context)
                    except: final_text = text_template
                    
                    # Doble salto de línea al inicio y fin para separar bien
                    rt_bloque_admin.add(f"\n\n{idx}. {key}\n", bold=True, size=32) 
                    rt_bloque_admin.add(self.html_to_richtext(final_text))
                    rt_bloque_admin.add("\n")
                    idx += 1

            # Inyectar el bloque de texto acumulado
            context["BLOQUE_ADMINISTRATIVO"] = rt_bloque_admin

            # --- BASES TÉCNICAS ---
            if "BASES TÉCNICAS" in TEXTOS_LEGALES and context.get("check_bases_tecnicas", 0):
                bt_text = TEXTOS_LEGALES["BASES TÉCNICAS"]
                try: bt_text = bt_text.format(**context)
                except: pass
                rt_bt = RichText()
                rt_bt.add("\n\nBASES TÉCNICAS\n", bold=True, size=36)
                rt_bt.add(self.html_to_richtext(bt_text))
                context["BASES TÉCNICAS"] = rt_bt
                context["mostrar_bases_tecnicas"] = True
            else:
                context["BASES TÉCNICAS"] = ""
                context["mostrar_bases_tecnicas"] = False

            # --- ANEXO 1: CALENDARIO (Formato Ficha) ---
            rt_anexos = RichText()
            rt_anexos.add("\nANEXO N°1: CALENDARIO DE LA PROPUESTA\n", bold=True, size=28)
            rt_anexos.add("-" * 60 + "\n")
            
            cal_data = context.get("calendario", [])
            if cal_data:
                for item in cal_data:
                    act = item.get("actividad", "Actividad")
                    ini = item.get("inicio", "-")
                    fin = item.get("termino", "-")
                    obs = item.get("obs", "")
                    
                    rt_anexos.add(f"ACTIVIDAD: {act}\n", bold=True, size=24)
                    rt_anexos.add(f"Inicio: {ini}   |   Término: {fin}\n", size=24)
                    if obs: rt_anexos.add(f"Observación: {obs}\n", size=24)
                    rt_anexos.add("-" * 60 + "\n")
            else:
                rt_anexos.add("[No se han definido actividades en el calendario]\n")

            context["ANEXOS_ADICIONALES"] = rt_anexos

            gen = DocumentGenerator(os.path.join(config.TEMPLATE_DIR, "plantilla_base.docx"))
            success, msg = gen.generar_word(context, output_path)
            if success:
                if self.current_session["licitacion_id"]: self.db.actualizar_ruta_archivo(self.current_session["licitacion_id"], output_path)
                return True
            else: QMessageBox.warning(self, "Error", msg); return False
        except Exception as e: print(f"Error: {e}"); QMessageBox.critical(self, "Error", str(e)); return False