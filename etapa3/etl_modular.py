import logging
import pandas as pd
from sqlalchemy import text
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'etapa2')))
from conexion_db import obtener_conexion_postgres, obtener_conexion_oracle

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def inicializar_tabla_control(conn_pg):
    """Crea la tabla de control y la sincroniza automáticamente con la realidad de los datos."""
    conn_pg.execute(text("""
        CREATE TABLE IF NOT EXISTS migracion_control (
            nombre_tabla VARCHAR(50) PRIMARY KEY,
            ultimo_id_procesado INT
        )
    """))
    
    # MAGIA AQUÍ: Buscamos el ID real que ya existe en tu tabla (si está vacía, devuelve 0)
    max_id_real = conn_pg.execute(text(
        "SELECT COALESCE(MAX(id_candidato), 0) FROM candidatos_ape"
    )).scalar()

    # Insertamos o actualizamos el registro con el ID real
    conn_pg.execute(text("""
        INSERT INTO migracion_control (nombre_tabla, ultimo_id_procesado)
        VALUES ('candidatos_ape', :max_id)
        ON CONFLICT (nombre_tabla) DO UPDATE 
        SET ultimo_id_procesado = :max_id
    """), {"max_id": max_id_real})

def obtener_ultimo_id(conn_pg) -> int:
    """Consulta el 'marcapáginas' para saber desde dónde reanudar."""
    resultado = conn_pg.execute(text(
        "SELECT ultimo_id_procesado FROM migracion_control WHERE nombre_tabla = 'candidatos_ape'"
    )).scalar()
    return resultado if resultado else 0

def actualizar_ultimo_id(conn_pg, ultimo_id: int):
    """Actualiza el 'marcapáginas' después de cada lote exitoso."""
    conn_pg.execute(text("""
        UPDATE migracion_control 
        SET ultimo_id_procesado = :uid 
        WHERE nombre_tabla = 'candidatos_ape'
    """), {"uid": ultimo_id})

def ejecutar_etl_con_reanudacion(tamano_lote: int = 2000):
    motor_pg = obtener_conexion_postgres()
    motor_or = obtener_conexion_oracle()

    with motor_pg.connect() as conn_pg:
        # 1. Preparamos el entorno usando un bloque transaccional limpio
        with conn_pg.begin():
            inicializar_tabla_control(conn_pg)

        # 2. Revisamos por dónde vamos
        ultimo_id = obtener_ultimo_id(conn_pg)
        conn_pg.commit()  # Cerramos la transacción de lectura automática
        
        logging.info(f"Iniciando ETL. Último ID migrado previamente: {ultimo_id}")

        with motor_or.connect() as conn_or:
            while True:
                # E: EXTRACT 
                logging.info(f"Extrayendo lote de {tamano_lote} registros desde el ID {ultimo_id}...")
                query_extract = text("""
                    SELECT id_candidato, nombre, profesion, estado 
                    FROM candidatos_ape 
                    WHERE id_candidato > :ultimo_id 
                    ORDER BY id_candidato ASC 
                    FETCH NEXT :lote ROWS ONLY
                """)
                
                resultado = conn_or.execute(query_extract, {"ultimo_id": ultimo_id, "lote": tamano_lote})
                datos = resultado.mappings().all()

                if not datos:
                    logging.info("No hay más datos para migrar. ETL Finalizado.")
                    break

                # T: TRANSFORM 
                df = pd.DataFrame(datos)
                df['nombre'] = df['nombre'].str.upper() 
                
                # L: LOAD (Usando el bloque 'with' para un manejo profesional de errores)
                try:
                    with conn_pg.begin():
                        datos_transformados = df.to_dict(orient='records')
                        
                        query_insert = text("""
                            INSERT INTO candidatos_ape (id_candidato, nombre, profesion, estado) 
                            VALUES (:id_candidato, :nombre, :profesion, :estado)
                        """)
                        
                        conn_pg.execute(query_insert, datos_transformados)
                        
                        nuevo_ultimo_id = int(df['id_candidato'].max())
                        actualizar_ultimo_id(conn_pg, nuevo_ultimo_id)
                    
                    # Si el código llega a esta línea, el commit se hizo exitosamente
                    ultimo_id = nuevo_ultimo_id
                    logging.info(f"Lote insertado con éxito. Marcapáginas actualizado al ID: {ultimo_id}")
                    
                    time.sleep(1) 
                    
                except Exception as e:
                    # El rollback ocurre de forma automática al fallar el bloque 'with'
                    logging.error(f"Error cargando el lote: {e}")
                    break

if __name__ == "__main__":
    ejecutar_etl_con_reanudacion(tamano_lote=2000)