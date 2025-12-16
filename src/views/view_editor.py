from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QTextEdit, QPushButton, QFrame, QMessageBox)
from PySide6.QtCore import Qt
from src.views.view_form import DocumentPreviewDialog

class EditorView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        self.setStyleSheet("""
            QWidget { background-color: #0f172a; color: #f1f5f9; font-family: 'Segoe UI', sans-serif; }
            QLabel.PageTitle { color: white; font-size: 24px; font-weight: 800; margin-bottom: 10px; }
            QLabel { color: #94a3b8; font-size: 14px; margin-bottom: 5px; }
            
            /* ESTILO TIPO WORD PARA EL EDITOR */
            QTextEdit { 
                background-color: white; 
                color: black; 
                border: 1px solid #cbd5e1; 
                border-radius: 2px; 
                padding: 40px; 
                font-family: 'Calibri', 'Arial', sans-serif; 
                font-size: 14px; 
                line-height: 1.5;
            }
            QTextEdit:focus { border: 2px solid #3b82f6; }
            
            QPushButton { padding: 10px 20px; border-radius: 6px; font-weight: bold; font-size: 14px; }
            QPushButton.Primary { background-color: #3b82f6; color: white; border: none; }
            QPushButton.Primary:hover { background-color: #2563eb; }
            QPushButton.Secondary { background-color: #475569; color: white; border: none; }
            QPushButton.Secondary:hover { background-color: #334155; }
        """)

        layout = QVBoxLayout(self); layout.setContentsMargins(30,30,30,30); layout.setSpacing(20)

        header = QHBoxLayout()
        lbl_title = QLabel("Redacción de Bases Técnicas")
        lbl_title.setProperty("class", "PageTitle")
        header.addWidget(lbl_title)
        header.addStretch()
        
        self.btn_preview = QPushButton("👁️ Ver Documento Completo")
        self.btn_preview.setCursor(Qt.PointingHandCursor)
        self.btn_preview.setProperty("class", "Secondary")
        self.btn_preview.clicked.connect(self.show_full_preview)
        header.addWidget(self.btn_preview)
        layout.addLayout(header)

        layout.addWidget(QLabel("Aquí puedes editar el contenido libre de las Bases Técnicas. El resto (caratula, legal, anexos) se genera automáticamente."))

        # EDITOR
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Escriba o pegue aquí el contenido de las Bases Técnicas...")
        self.editor.setAcceptRichText(True) 
        layout.addWidget(self.editor)

        bot_layout = QHBoxLayout()
        btn_back = QPushButton("❮ Volver al Formulario")
        btn_back.setCursor(Qt.PointingHandCursor)
        btn_back.setProperty("class", "Secondary")
        btn_back.clicked.connect(self.go_back)
        
        btn_save = QPushButton("Guardar Cambios")
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.setProperty("class", "Primary")
        btn_save.clicked.connect(self.save_data)

        bot_layout.addWidget(btn_back)
        bot_layout.addStretch()
        bot_layout.addWidget(btn_save)
        layout.addLayout(bot_layout)

    def load_data_variables(self):
        d = self.controller.current_session.get("data", {})
        content = d.get("bases_tecnicas_editadas", "")
        
        if not content:
            from src.data.base_texts import TEXTOS_LEGALES
            content = TEXTOS_LEGALES.get("BASES TÉCNICAS", "")
            try: content = content.format(**d)
            except: pass
            content = content.replace("\n", "<br>")

        self.editor.setHtml(str(content))

    def save_data(self):
        html_content = self.editor.toHtml()
        plain_text = self.editor.toPlainText()

        update_data = {
            "bases_tecnicas_editadas": plain_text, 
            "bases_tecnicas_html": html_content
        }
        
        self.controller.save_session_data(update_data)
        QMessageBox.information(self, "Guardado", "Bases Técnicas actualizadas.")

    def show_full_preview(self):
        self.save_data() 
        html = self.controller.generate_preview_html()
        DocumentPreviewDialog(html, self).exec()

    def go_back(self):
        self.controller.cambiar_vista("form")