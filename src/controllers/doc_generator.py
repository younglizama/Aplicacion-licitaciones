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
        Rellena la plantilla procesando recursivamente todo el texto a RichText
        para respetar los saltos de línea en Word, incluso dentro de listas o diccionarios.
        """
        try:
            # 1. Cargar la plantilla
            self.doc = DocxTemplate(self.template_path)
            
            # --- FUNCIÓN AUXILIAR RECURSIVA ---
            # Convierte strings a RichText y recorre listas/diccionarios
            def process_context(data):
                if isinstance(data, str):
                    # RichText asegura que los \n se conviertan en saltos de línea reales en Word
                    return RichText(data)
                elif isinstance(data, list):
                    return [process_context(item) for item in data]
                elif isinstance(data, dict):
                    return {k: process_context(v) for k, v in data.items()}
                return data
            # ----------------------------------

            # 2. Procesar todos los datos (incluyendo calendario y otros sub-items)
            final_context = process_context(context_data)
            
            # 3. Renderizar (Inyectar datos procesados)
            self.doc.render(final_context)
            
            # 4. Guardar
            self.doc.save(output_path)
            
            return True, f"Documento generado exitosamente en:\n{output_path}"

        except PermissionError:
            return False, "Error de Permisos: El archivo de destino parece estar abierto. Ciérrelo e intente nuevamente."
        except Exception as e:
            return False, f"Ocurrió un error inesperado:\n{str(e)}"