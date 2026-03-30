import sys
import os
from sqlalchemy import text

# Importamos tu función de conexión a PostgreSQL
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'etapa2')))
from conexion_db import obtener_conexion_postgres

def limpiar_base_de_datos():
    print("Conectando a PostgreSQL para resetear el entorno...")
    motor_pg = obtener_conexion_postgres()
    
    try:
        with motor_pg.connect() as conn:
            with conn.begin():
                # Vaciamos ambas tablas en una sola transacción segura
                print("Vaciando la tabla 'candidatos_ape'...")
                conn.execute(text("TRUNCATE TABLE candidatos_ape;"))
                
                print("Vaciando la tabla 'migracion_control'...")
                conn.execute(text("TRUNCATE TABLE migracion_control;"))
                
        print("¡Éxito! Base de datos completamente limpia y lista para la prueba de caída.")
    except Exception as e:
        print(f"Ocurrió un error al intentar limpiar la base de datos: {e}")

if __name__ == "__main__":
    limpiar_base_de_datos()