import os
import re
import platform
import subprocess
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

    # --- GENERADOR DE VISTA PREVIA (HTML) ---
    def generate_preview_html(self):
        d = self.current_session["data"]
        
        css = """<style>
            body { font-family: 'Calibri', 'Arial', sans-serif; font-size: 11pt; line-height: 1.15; color: #000; padding: 40px; background-color: white; }
            h1 { text-align: center; font-size: 16pt; margin: 20px 0; text-transform: uppercase; color: #000; font-weight: bold; border-bottom: 1px solid #000; padding-bottom: 10px; }
            h2 { font-size: 12pt; margin-top: 20px; margin-bottom: 10px; text-transform: uppercase; font-weight: bold; color: #000; }
            p, li { margin-bottom: 8px; text-align: justify; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 10pt; }
            td, th { border: 1px solid #000; padding: 4px 8px; vertical-align: top; }
            .th-head { background-color: #d9d9d9; font-weight: bold; text-align: center; }
            .gray-col { background-color: #f2f2f2; font-weight: bold; width: 35%; }
            .info-header { text-align: center; font-weight: bold; margin-bottom: 20px; font-size: 14pt; }
        </style>"""
        
        html = f"{css}<body>"
        
        html += f"<div class='info-header'>LICITACIÓN {d.get('nombre_adquisicion','').upper()}<br>BASES ADMINISTRATIVAS</div>"
        html += f"<p>Isapre Fundación Banco Estado, en adelante “la Isapre”, invita a participar en una {d.get('tipo_licitacion','')}...</p>"

        # TABLA DE CARACTERÍSTICAS
        if d.get("razon_social"):
            html += "<table>"
            html += f"<tr><td class='gray-col'>Razón Social</td><td>{d.get('razon_social','')}</td></tr>"
            html += f"<tr><td class='gray-col'>RUT</td><td>{d.get('rut_empresa','')}</td></tr>"
            html += f"<tr><td class='gray-col'>Comuna</td><td>{d.get('comuna','')}</td></tr>"
            html += f"<tr><td class='gray-col'>Región</td><td>{d.get('region','')}</td></tr>"
            html += f"<tr><td class='gray-col'>Nombre de Adquisición</td><td>{d.get('nombre_adquisicion','')}</td></tr>"
            html += f"<tr><td class='gray-col'>Descripción</td><td>{d.get('descripcion','')}</td></tr>"
            html += f"<tr><td class='gray-col'>Duración de contrato</td><td>{d.get('duracion_contrato','')}</td></tr>"
            html += f"<tr><td class='gray-col'>Tipo de licitación</td><td>{d.get('tipo_licitacion','')}</td></tr>"
            html += f"<tr><td class='gray-col'>Moneda</td><td>{d.get('moneda','')}</td></tr>"
            html += "</table>"

        idx = 1
        ORDERED_KEYS = [
            "OBJETIVOS", "DEFINICIONES", 
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

        for key in ORDERED_KEYS:
            checkbox_key = "check_" + key.lower().replace(" ","_").replace(",","").replace(".","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("/","_")
            if not d.get(checkbox_key, 0): continue

            if key == "GARANTÍAS":
                html += f"<h2>{idx}. GARANTÍAS</h2>"
                
                html += "<p><b>Seriedad de la Oferta:</b></p>"
                html += "<table>"
                html += f"<tr><td class='gray-col'>Tipo de Documento</td><td>Boleta de Garantía o Póliza de Seguro</td></tr>"
                html += f"<tr><td class='gray-col'>Beneficiario</td><td>{d.get('organismo','Isapre Fundación Banco Estado')}</td></tr>"
                html += f"<tr><td class='gray-col'>Rut</td><td>{d.get('rut_empresa','')}</td></tr>"
                html += f"<tr><td class='gray-col'>Fecha de Vencimiento</td><td>{d.get('vencimiento_seriedad','')}</td></tr>"
                html += f"<tr><td class='gray-col'>Monto</td><td>{d.get('monto_seriedad','')}</td></tr>"
                html += f"<tr><td class='gray-col'>Glosa</td><td>Para garantizar la seriedad de la oferta de la Licitación</td></tr>"
                html += "</table>"
                
                html += "<p><b>Fiel Cumplimiento del Contrato:</b></p>"
                html += "<table>"
                html += f"<tr><td class='gray-col'>Tipo de Documento</td><td>Boleta de Garantía o Póliza de Seguro</td></tr>"
                html += f"<tr><td class='gray-col'>Beneficiario</td><td>{d.get('organismo','Isapre Fundación Banco Estado')}</td></tr>"
                html += f"<tr><td class='gray-col'>Rut</td><td>{d.get('rut_empresa','')}</td></tr>"
                html += f"<tr><td class='gray-col'>Fecha de Vencimiento</td><td>{d.get('vencimiento_cumplimiento','')}</td></tr>"
                html += f"<tr><td class='gray-col'>Monto</td><td>{d.get('monto_cumplimiento','')}</td></tr>"
                html += f"<tr><td class='gray-col'>Glosa</td><td>Para garantizar el fiel cumplimiento del contrato</td></tr>"
                html += "</table>"
                idx += 1

            elif key == "EVALUACIÓN Y ADJUDICACIÓN DE LAS OFERTAS":
                html += f"<h2>{idx}. EVALUACIÓN Y ADJUDICACIÓN DE LAS OFERTAS</h2>"
                html += "<ul>"
                html += f"<li>Oferta Económica: {d.get('eval_economica','0')}%</li>"
                html += f"<li>Oferta Técnica: {d.get('eval_tecnica','0')}%</li>"
                html += f"<li>Experiencia: {d.get('eval_experiencia','0')}%</li>"
                for c in d.get('extra_criteria', []):
                    html += f"<li>{c['name']}: {c['pct']}%</li>"
                html += "</ul>"
                idx += 1
            else:
                html += f"<h2>{idx}. {key}</h2>"
                txt = TEXTOS_LEGALES.get(key, "")
                try: txt = txt.format(**d)
                except: pass
                html += f"<div>{txt}</div>"
                idx += 1

        if d.get("check_bases_tecnicas"):
             html += "<h2>BASES TÉCNICAS</h2>"
             bt_text = d.get("bases_tecnicas_editadas") or TEXTOS_LEGALES.get("BASES TÉCNICAS", "")
             try: bt_text = bt_text.format(**d)
             except: pass
             html += f"<div>{bt_text}</div>"

        html += "<br><h2>ANEXO N°1: CALENDARIO DE LA PROPUESTA</h2>"
        html += "<table>"
        html += "<tr><th class='th-head' style='width: 40%;'>ACTIVIDAD</th><th class='th-head'>INICIO</th><th class='th-head'>TÉRMINO</th><th class='th-head'>OBSERVACIÓN</th></tr>"
        for item in d.get("calendario", []):
            html += f"<tr><td>{item.get('actividad','')}</td><td>{item.get('inicio','')}</td><td>{item.get('termino','')}</td><td>{item.get('obs','')}</td></tr>"
        html += "</table></body>"
        
        return html

    # --- GENERADOR DOCX ---
    def generate_docx(self, output_path):
        try:
            print(f"🚀 Generando DOCX en: {output_path}")
            context = self.current_session["data"].copy()

            if 'duracion_contrato' in context: context['duración_contrato'] = context['duracion_contrato']
            
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
            rt_bloque_admin = RichText() 

            for key in ORDERED_KEYS:
                checkbox_key = "check_" + key.lower().replace(" ","_").replace(",","").replace(".","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("/","_")
                show_key = f"mostrar_{checkbox_key.replace('check_', '')}"
                
                if not context.get(checkbox_key, 0): 
                    context[key] = ""; context[show_key] = False; continue
                
                context[show_key] = True

                if key == "CARACTERÍSTICAS DE LA LICITACIÓN": pass 
                elif key == "GARANTÍAS":
                    # TAMAÑO CORREGIDO: size=28 (aprox 14pt)
                    rt = RichText(); rt.add(f"{idx}. {key}", bold=True, size=28); context["GARANTÍAS"] = rt; idx += 1
                elif key == "EVALUACIÓN Y ADJUDICACIÓN DE LAS OFERTAS":
                    # TAMAÑOS CORREGIDOS
                    rt = RichText(); rt.add(f"{idx}. {key}\n", bold=True, size=28)
                    rt.add("Ponderación de Criterios:\n", bold=True, size=22)
                    rt.add(f"• Económica: {context.get('eval_economica','0')}%\n", size=22)
                    rt.add(f"• Técnica: {context.get('eval_tecnica','0')}%\n", size=22)
                    rt.add(f"• Experiencia: {context.get('eval_experiencia','0')}%\n", size=22)
                    if context.get('extra_criteria'):
                         for c in context.get('extra_criteria'): rt.add(f"• {c.get('name')}: {c.get('pct')}%\n", size=22)
                    rt.add("\nAdjudicación al mayor puntaje.", size=22)
                    context["EVALUACIÓN_Y_ADJUDICACIÓN_DE_LAS_OFERTAS"] = rt
                    idx += 1
                else:
                    text_template = TEXTOS_LEGALES.get(key, "")
                    try: final_text = text_template.format(**context)
                    except: final_text = text_template
                    # TAMAÑO CORREGIDO: size=28
                    rt_bloque_admin.add(f"\n\n{idx}. {key}\n", bold=True, size=28) 
                    rt_bloque_admin.add(self.html_to_richtext(final_text)); rt_bloque_admin.add("\n"); idx += 1

            context["BLOQUE_ADMINISTRATIVO"] = rt_bloque_admin

            if "BASES TÉCNICAS" in TEXTOS_LEGALES and context.get("check_bases_tecnicas", 0):
                bt_text = context.get("bases_tecnicas_editadas") or TEXTOS_LEGALES["BASES TÉCNICAS"]
                try: bt_text = bt_text.format(**context)
                except: pass
                # TAMAÑO CORREGIDO: size=32
                rt_bt = RichText(); rt_bt.add("\n\nBASES TÉCNICAS\n", bold=True, size=32); rt_bt.add(self.html_to_richtext(bt_text))
                context["BASES TÉCNICAS"] = rt_bt; context["mostrar_bases_tecnicas"] = True
            else:
                context["BASES TÉCNICAS"] = ""; context["mostrar_bases_tecnicas"] = False

            # Validar calendario
            calendario_data = context.get("calendario", [])
            if not isinstance(calendario_data, list): calendario_data = []
            context["calendario"] = calendario_data
            context["ANEXOS_ADICIONALES"] = "" 

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