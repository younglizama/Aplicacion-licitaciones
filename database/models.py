# Archivo generado automáticamente
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Licitacion:
    """Modelo de datos para una licitación. Facilita el manejo de datos estructurados."""
    id: Optional[int] = None
    folio: str = ""
    nombre: str = ""
    empresa: str = ""
    fecha_creacion: str = ""
    estado: str = "Borrador"
    ruta_archivo: str = ""
    # Aquí guardamos el diccionario completo del formulario
    datos_json: Dict[str, Any] = field(default_factory=dict)

    def resumen(self):
        return f"{self.folio} - {self.nombre} ({self.estado})"