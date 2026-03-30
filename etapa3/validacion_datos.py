import logging
import pandas as pd
from sqlalchemy import text
import sys
import os
import hashlib

# Importamos las conexiones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'etapa2')))
from conexion_db import obtener_conexion_postgres, obtener_conexion_oracle

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def validar_migracion():
    motor_pg = obtener_conexion_postgres()
    motor_or = obtener_conexion_oracle()

    logging.info("--- INICIANDO VALIDACIÓN DE DATOS ---")

    with motor_or.connect() as conn_or, motor_pg.connect() as conn_pg:
        # 1. CONTEOS CRUZADOS
        logging.info("1. Realizando conteos cruzados...")
        conteo_or = conn_or.execute(text("SELECT COUNT(*) FROM candidatos_ape")).scalar()
        conteo_pg = conn_pg.execute(text("SELECT COUNT(*) FROM candidatos_ape")).scalar()

        logging.info(f"   -> Total en Oracle: {conteo_or}")
        logging.info(f"   -> Total en PostgreSQL: {conteo_pg}")

        if conteo_or == conteo_pg:
            logging.info("RESULTADO: Los conteos coinciden perfectamente.")
        else:
            logging.error("RESULTADO: Discrepancia en la cantidad de registros.")

        # 2. HASH Y CHECKSUM (Validación de Integridad)
        logging.info("\n2. Generando Checksum para validar integridad...")
        
        # Extraemos los datos ordenados para asegurar que se comparen igual
        query = "SELECT id_candidato, nombre, profesion, estado FROM candidatos_ape ORDER BY id_candidato"
        df_or = pd.read_sql(query, conn_or)
        df_pg = pd.read_sql(query, conn_pg)

        # Generamos un hash MD5 de todo el DataFrame
        hash_or = hashlib.md5(pd.util.hash_pandas_object(df_or, index=True).values).hexdigest()
        hash_pg = hashlib.md5(pd.util.hash_pandas_object(df_pg, index=True).values).hexdigest()

        logging.info(f"   -> Hash Origen (Oracle):     {hash_or}")
        logging.info(f"   -> Hash Destino (PostgreSQL): {hash_pg}")

        if hash_or == hash_pg:
            logging.info("RESULTADO: La integridad de los datos es perfecta. Ningún dato sufrió alteraciones.")
        else:
            logging.error("RESULTADO: Los datos son diferentes (Los hashes no coinciden).")

if __name__ == "__main__":
    validar_migracion()