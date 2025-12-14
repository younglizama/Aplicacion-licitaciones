import sqlite3
import json
import os
from datetime import datetime
import config

class DBManager:
    def __init__(self):
        self.db_path = os.path.join(config.BASE_DIR, "licitaciones.db")

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Agregamos columna 'ruta_archivo'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS licitaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                folio TEXT,
                nombre TEXT,
                empresa TEXT,
                fecha_creacion TEXT,
                estado TEXT,
                ruta_archivo TEXT,
                datos_json TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def get_next_id(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT seq FROM sqlite_sequence WHERE name='licitaciones'")
        row = cursor.fetchone()
        conn.close()
        return (row[0] + 1) if row else 1

    def guardar_licitacion(self, data_dict, licitacion_id=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        folio = f"LIC-{datetime.now().year}-{self.get_next_id():03d}" if not licitacion_id else data_dict.get("folio", "S/F")
        nombre = data_dict.get("nombre_adquisicion", "Sin Nombre")
        empresa = data_dict.get("organismo", "Sin Empresa")
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        estado = "Borrador"
        json_data = json.dumps(data_dict)

        if licitacion_id:
            cursor.execute('''
                UPDATE licitaciones 
                SET nombre=?, empresa=?, fecha_creacion=?, datos_json=?
                WHERE id=?
            ''', (nombre, empresa, fecha, json_data, licitacion_id))
            saved_id = licitacion_id
        else:
            cursor.execute('''
                INSERT INTO licitaciones (folio, nombre, empresa, fecha_creacion, estado, datos_json)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (folio, nombre, empresa, fecha, estado, json_data))
            saved_id = cursor.lastrowid

        conn.commit()
        conn.close()
        return saved_id

    def actualizar_ruta_archivo(self, licitacion_id, ruta):
        """Guarda la ubicación del Word generado"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE licitaciones SET ruta_archivo=?, estado='Generado' WHERE id=?", (ruta, licitacion_id))
        conn.commit()
        conn.close()

    def get_all_licitaciones(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM licitaciones ORDER BY id DESC")
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows

    def get_licitacion_by_id(self, lic_id):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM licitaciones WHERE id=?", (lic_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            data = dict(row)
            data["datos_json"] = json.loads(data["datos_json"])
            return data
        return None

    def delete_licitacion(self, lic_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM licitaciones WHERE id=?", (lic_id,))
        conn.commit()
        conn.close()