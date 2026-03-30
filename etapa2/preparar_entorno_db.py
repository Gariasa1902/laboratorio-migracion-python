import logging
from sqlalchemy import text
# Importamos las funciones de conexión del archivo anterior
from conexion_db import obtener_conexion_postgres, obtener_conexion_oracle

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preparar_bases_de_datos():
    motor_pg = obtener_conexion_postgres()
    motor_or = obtener_conexion_oracle()

    # 1. Preparar PostgreSQL (Destino)
    try:
        with motor_pg.connect() as conn_pg:
            # Iniciamos transacción explícita
            trans = conn_pg.begin()
            logging.info("Creando tabla 'candidatos_ape' en PostgreSQL...")
            conn_pg.execute(text("""
                CREATE TABLE IF NOT EXISTS candidatos_ape (
                    id_candidato INT PRIMARY KEY,
                    nombre VARCHAR(100),
                    profesion VARCHAR(100),
                    estado VARCHAR(20)
                )
            """))
            # Limpiamos la tabla por si ya tenía datos de pruebas anteriores
            conn_pg.execute(text("TRUNCATE TABLE candidatos_ape"))
            trans.commit()
            logging.info("Tabla en PostgreSQL lista y limpia.")
    except Exception as e:
        logging.error(f"Error en PostgreSQL: {e}")

    # 2. Preparar Oracle (Origen)
    try:
        with motor_or.connect() as conn_or:
            trans = conn_or.begin()
            
            # En Oracle, si la tabla existe y la intentamos crear, da error. 
            # Capturamos esa excepción específica de forma silenciosa.
            try:
                conn_or.execute(text("""
                    CREATE TABLE candidatos_ape (
                        id_candidato NUMBER PRIMARY KEY,
                        nombre VARCHAR2(100),
                        profesion VARCHAR2(100),
                        estado VARCHAR2(20)
                    )
                """))
                logging.info("Tabla 'candidatos_ape' creada en Oracle.")
            except Exception:
                logging.info("La tabla en Oracle ya existe. Limpiando datos...")
                conn_or.execute(text("TRUNCATE TABLE candidatos_ape"))

            # Insertamos datos de prueba en Oracle (Queries parametrizadas)
            logging.info("Insertando datos de prueba en Oracle...")
            query_insert = text("""
                INSERT INTO candidatos_ape (id_candidato, nombre, profesion, estado) 
                VALUES (:id, :nom, :prof, :est)
            """)
            
            # Lista de diccionarios con los parámetros a insertar
            datos = [
                {"id": 1, "nom": "Ana García", "prof": "Desarrolladora Go", "est": "Activo"},
                {"id": 2, "nom": "Luis Pérez", "prof": "Analista de Datos", "est": "Pendiente"},
                {"id": 3, "nom": "Marta Rojas", "prof": "DevOps", "est": "Activo"}
            ]
            
            for dato in datos:
                conn_or.execute(query_insert, dato)
                
            trans.commit()
            logging.info("Datos de prueba insertados en Oracle con éxito.")
    except Exception as e:
        logging.error(f"Error en Oracle: {e}")

if __name__ == "__main__":
    preparar_bases_de_datos()