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

            for key, text_template in TEXTOS_LEGALES.items():
                checkbox_key = "check_" + key.lower().replace(" ","_").replace(",","").replace(".","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("/","_")
                show_key = f"mostrar_{checkbox_key.replace('check_', '')}"
                if not context.get(checkbox_key, 0): context[key] = ""; context[show_key] = False; continue
                context[show_key] = True

                if key == "CARACTERÍSTICAS DE LA LICITACIÓN":
                    rt = RichText(); rt.add("CARACTERÍSTICAS DE LA LICITACIÓN\n", bold=True, size=24)
                    rt.add(f"• Razón Social: {context.get('razon_social','')}\n• RUT: {context.get('rut_empresa','')}\n• Comuna: {context.get('comuna','')}\n• Región: {context.get('region','')}\n• Nombre: {context.get('nombre_adquisicion','')}\n• Descripción: {context.get('descripcion','')}\n• Duración: {context.get('duracion_contrato','')}\n• Tipo: {context.get('tipo_licitacion','')}\n• Moneda: {context.get('moneda','')}")
                    context[key] = rt
                elif key == "GARANTÍAS":
                    rt = RichText(); rt.add("GARANTÍAS\n", bold=True, size=24)
                    rt.add("Seriedad de la Oferta:\n", bold=True, underline=True); rt.add(f"• Monto: ${context.get('monto_seriedad','0')}\n• Vencimiento: {context.get('vencimiento_seriedad','')}\n\n")
                    rt.add("Fiel Cumplimiento:\n", bold=True, underline=True); rt.add(f"• Monto: ${context.get('monto_cumplimiento','0')}\n• Vencimiento: {context.get('vencimiento_cumplimiento','')}")
                    context[key] = rt
                elif key == "EVALUACIÓN Y ADJUDICACIÓN DE LAS OFERTAS":
                    rt = RichText(); rt.add("EVALUACIÓN Y ADJUDICACIÓN DE LAS OFERTAS\n", bold=True, size=24)
                    rt.add("Ponderación de Criterios:\n", bold=True); rt.add(f"• Económica: {context.get('eval_economica','0')}%\n• Técnica: {context.get('eval_tecnica','0')}%\n• Experiencia: {context.get('eval_experiencia','0')}%\n")
                    if context.get('otros_criterios'):
                         for l in str(context.get('otros_criterios','')).split('\n'): 
                             if l.strip(): rt.add(f"• {l.replace('-','').strip()}\n")
                    rt.add("\nAdjudicación al mayor puntaje.")
                    context[key] = rt
                else:
                    try: final_text = text_template.format(**context)
                    except: final_text = text_template
                    
                    # --- CORRECCIÓN INDICES (TITULOS EN NEGRITA) ---
                    rt_final = RichText(); rt_final.add(f"{key}\n", bold=True, size=24)
                    rt_final.add(self.html_to_richtext(final_text))
                    context[key] = rt_final

            # --- ANEXO 1 CON 4 CAMPOS ---
            rt_anexos = RichText()
            rt_anexos.add("\nANEXO N°1: CALENDARIO DE LA PROPUESTA\n", bold=True, size=24)
            
            cal_data = context.get("calendario", [])
            if cal_data:
                for item in cal_data:
                    act = item.get("actividad", "Actividad")
                    ini = item.get("inicio", "-")
                    fin = item.get("termino", "-")
                    obs = item.get("obs", "")
                    
                    rt_anexos.add(f"• {act}: ", bold=True)
                    info = f"Del {ini} al {fin}"
                    if obs: info += f" ({obs})"
                    rt_anexos.add(f"{info}\n")
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