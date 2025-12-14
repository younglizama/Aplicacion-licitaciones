from docxtpl import DocxTemplate, RichText
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
        Rellena la plantilla respetando los saltos de línea y el formato.
        """
        try:
            # 1. Cargar la plantilla
            self.doc = DocxTemplate(self.template_path)
            
            # 2. PROCESAMIENTO INTELIGENTE DE FORMATO
            # Recorremos todos los datos. Si es texto, lo convertimos a RichText
            # para que Word respete los "Enter" (saltos de línea).
            final_context = {}
            
            for key, value in context_data.items():
                if isinstance(value, str):
                    # RichText asegura que los \n se conviertan en saltos de línea reales en Word
                    rt = RichText(value)
                    final_context[key] = rt
                else:
                    final_context[key] = value
            
            # 3. Renderizar (Inyectar datos procesados)
            self.doc.render(final_context)
            
            # 4. Guardar
            self.doc.save(output_path)
            
            return True, f"Documento generado exitosamente en:\n{output_path}"

        except PermissionError:
            return False, "Error de Permisos: El archivo de destino parece estar abierto. Ciérrelo e intente nuevamente."
        except Exception as e:
            return False, f"Ocurrió un error inesperado:\n{str(e)}"