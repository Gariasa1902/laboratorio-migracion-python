import logging
from sqlalchemy import text
import sys
import os

# Agregamos la ruta del proyecto para poder importar conexion_db de la etapa2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'etapa2')))
from conexion_db import obtener_conexion_oracle

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def generar_datos_masivos():
    motor_or = obtener_conexion_oracle()
    
    logging.info("Generando 10,000 registros de prueba en Oracle...")
    try:
        with motor_or.connect() as conn:
            trans = conn.begin()
            # Limpiamos la tabla primero
            conn.execute(text("TRUNCATE TABLE candidatos_ape"))
            
            query = text("""
                INSERT INTO candidatos_ape (id_candidato, nombre, profesion, estado) 
                VALUES (:id, :nom, :prof, :est)
            """)
            
            # Generamos lotes de datos en memoria para insertarlos rápidamente
            datos = [
                {"id": i, "nom": f"Candidato_{i}", "prof": "Ingeniero", "est": "Activo"} 
                for i in range(1, 10001)
            ]
            
            conn.execute(query, datos)
            trans.commit()
            logging.info("¡10,000 registros insertados en Oracle con éxito!")
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    generar_datos_masivos()