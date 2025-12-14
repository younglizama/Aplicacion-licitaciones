from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox
from PySide6.QtCore import Qt

# --- IMPORTACIÓN DE VISTAS ---
from src.views.view_welcome import WelcomeView
from src.views.view_form import FormView
from src.views.view_editor import EditorView
from src.views.view_files import FilesView
from src.views.view_chat import ChatView

# --- IMPORTACIÓN DE BASE DE DATOS ---
from database.db_manager import DBManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 1. Configuración de la Ventana
        self.setWindowTitle("Sistema de Gestión de Licitaciones - Isapre Fundación")
        self.resize(1300, 850)
        self.setMinimumSize(1000, 700)
        
        # 2. Inicializar Base de Datos
        # La instancia se comparte con todas las vistas hijas
        self.db = DBManager()
        self.db.init_db()
        
        # 3. Estado de la Sesión Actual
        # Aquí guardamos el ID de la licitación que se está editando
        self.current_session = {
            "licitacion_id": None, 
            "data": {}             
        }

        # 4. Gestor de Vistas (QStackedWidget)
        # Funciona como un libro: solo muestra una página a la vez
        self.central_stack = QStackedWidget()
        self.setCentralWidget(self.central_stack)

        # 5. Instanciar y Registrar Vistas
        # Pasamos 'self' (MainWindow) como controlador
        self.view_welcome = WelcomeView(self) # Índice 0
        self.view_form = FormView(self)       # Índice 1
        self.view_editor = EditorView(self)   # Índice 2
        self.view_files = FilesView(self)     # Índice 3

        self.central_stack.addWidget(self.view_welcome)
        self.central_stack.addWidget(self.view_form)
        self.central_stack.addWidget(self.view_editor)
        self.central_stack.addWidget(self.view_files)

        # 6. Configuración del Copiloto IA (Chat)
        # Se maneja aquí para que flote sobre toda la ventana
        try:
            self.chat_helper = ChatView(self)
        except Exception as e:
            print(f"⚠️ Advertencia: No se pudo cargar el chat: {e}")
            self.chat_helper = None

        # Iniciar en la pantalla de Bienvenida
        self.cambiar_vista("welcome")

    def cambiar_vista(self, view_name):
        """
        Gestor central de navegación.
        Controla qué vista se muestra y la visibilidad del botón de Chat.
        """
        # --- Lógica de Navegación ---
        if view_name == "welcome":
            self.central_stack.setCurrentIndex(0)
            self._set_chat_visible(False) # Ocultar chat en inicio

        elif view_name == "form":
            self.central_stack.setCurrentIndex(1)
            self.view_form.load_existing_data() # Recargar datos si volvemos atrás
            self._set_chat_visible(True)

        elif view_name == "editor":
            self.central_stack.setCurrentIndex(2)
            # Actualizar editor con datos nuevos del form
            self.view_editor.load_data_variables() 
            self.view_editor.init_content_structure()
            self._set_chat_visible(True)

        elif view_name == "files":
            self.central_stack.setCurrentIndex(3)
            self.view_files.load_history() # Recargar tabla
            self._set_chat_visible(True)

    def _set_chat_visible(self, visible):
        """Helper para mostrar/ocultar el botón flotante del chat"""
        if self.chat_helper and hasattr(self.chat_helper, 'fab'):
            if visible:
                self.chat_helper.fab.show()
                self.chat_helper.fab.raise_() # Asegurar que esté encima de todo
            else:
                self.chat_helper.fab.hide()
                # Si la ventana del chat está abierta, cerrarla también
                if self.chat_helper.is_open:
                    self.chat_helper.close_chat()

    def start_new_licitacion(self):
        """Reinicia la sesión y manda al Formulario de datos"""
        self.current_session["licitacion_id"] = None
        self.current_session["data"] = {}
        print("🔄 Sesión reiniciada: Nueva Licitación")
        
        # Limpiar formulario visualmente (opcional, ya que load_existing_data lo hace)
        # self.view_form.limpiar_inputs() 
        
        self.cambiar_vista("form")

    def save_session_data(self, form_data):
        """
        Guarda los datos parciales en la Base de Datos SQLite.
        Es llamado por FormView y EditorView.
        """
        # 1. Actualizar memoria
        self.current_session["data"].update(form_data)
        current_id = self.current_session["licitacion_id"]
        
        # 2. Guardar en BD
        saved_id = self.db.guardar_licitacion(self.current_session["data"], current_id)
        
        # 3. Actualizar ID si es nuevo
        if current_id is None and saved_id:
            self.current_session["licitacion_id"] = saved_id
            print(f"✅ Licitación creada con ID: {saved_id}")
        else:
            print(f"💾 Licitación {current_id} actualizada.")
            
        return saved_id