from docxtpl import DocxTemplate
import os

class DocumentGenerator:
    def __init__(self, template_path):
        """
        Inicializa el generador con la ruta de la plantilla.
        """
        self.template_path = template_path
        self.doc = None
        
        # Validar que la plantilla existe
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"No se encontró la plantilla en: {self.template_path}")

    def generar_word(self, context_data, output_path):
        """
        Rellena la plantilla directamente con el diccionario de datos.
        """
        try:
            # 1. Cargar la plantilla
            self.doc = DocxTemplate(self.template_path)
            
            # 2. Renderizar (Inyectar datos crudos)
            # docxtpl se encarga de todo. No necesitamos convertir nada a RichText
            # a menos que lo hayamos hecho explícitamente en el main_window.
            self.doc.render(context_data)
            
            # 3. Guardar
            self.doc.save(output_path)
            
            return True, f"Documento generado exitosamente en:\n{output_path}"

        except PermissionError:
            return False, "Error de Permisos: El archivo de destino parece estar abierto. Ciérrelo e intente nuevamente."
        except Exception as e:
            return False, f"Ocurrió un error inesperado:\n{str(e)}"