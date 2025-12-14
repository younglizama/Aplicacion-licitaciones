import time
import threading
import google.generativeai as genai

class ChatController:
    def __init__(self):
        # --- CONFIGURACIÓN DE GEMINI ---
        self.api_key = "AIzaSyBfKGf5GDGQL3g5tTyIkJ7K0suPzJwU-nM"
        self.model = None
        
        try:
            genai.configure(api_key=self.api_key)
            
            # --- AUTO-DETECCIÓN DE MODELO ---
            # Buscamos en tu cuenta qué modelos sirven para chatear
            available_models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
            
            # Intentamos priorizar el más rápido (Flash), luego el Pro, luego cualquiera
            model_name = None
            if any("flash" in m for m in available_models):
                model_name = next(m for m in available_models if "flash" in m)
            elif any("gemini-1.5" in m for m in available_models):
                model_name = next(m for m in available_models if "gemini-1.5" in m)
            elif any("gemini-pro" in m for m in available_models):
                model_name = next(m for m in available_models if "gemini-pro" in m)
            else:
                model_name = available_models[0] if available_models else None

            if model_name:
                self.model = genai.GenerativeModel(model_name)
                print(f"✅ Conectado exitosamente usando el modelo: {model_name}")
            else:
                print("⚠️ No se encontraron modelos compatibles en tu cuenta.")

        except Exception as e:
            print(f"⚠️ Error al configurar Gemini: {e}")

        self.system_prompt = (
            "Actúa como un experto en Licitaciones Públicas de Chile. "
            "Ayudas a redactar textos formales y técnicos. "
            "Sé breve, profesional y directo."
        )

    def get_response(self, user_message, callback):
        thread = threading.Thread(target=self._worker, args=(user_message, callback))
        thread.start()

    def _worker(self, user_message, callback):
        try:
            if self.model is None:
                callback("⚠️ Error: No pude encontrar un modelo de IA compatible. Intenta actualizar la librería: pip install --upgrade google-generativeai")
                return

            full_prompt = f"{self.system_prompt}\n\nUsuario: {user_message}"
            response = self.model.generate_content(full_prompt)
            
            if response and response.text:
                callback(response.text)
            else:
                callback("La IA no devolvió respuesta. Intenta de nuevo.")

        except Exception as e:
            callback(f"⚠️ Error de conexión: {str(e)}")