import logging
from sqlalchemy import text
from conexion_db import obtener_conexion_postgres, obtener_conexion_oracle

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def migrar_datos():
    motor_pg = obtener_conexion_postgres()
    motor_or = obtener_conexion_oracle()

    datos_extraidos = []

    # PASO 1: Extracción (Extract) de Oracle
    logging.info("Iniciando extracción desde Oracle...")
    try:
        with motor_or.connect() as conn_or:
            # Ejecutamos la consulta para traer todos los registros
            resultado = conn_or.execute(text("SELECT id_candidato, nombre, profesion, estado FROM candidatos_ape"))
            
            # Convertimos el resultado en una lista de diccionarios para facilitar su manejo
            # mappings() mapea automáticamente los nombres de las columnas con sus valores
            datos_extraidos = resultado.mappings().all()
            logging.info(f"Se extrajeron {len(datos_extraidos)} registros de Oracle.")
    except Exception as e:
        logging.error(f"Error durante la extracción: {e}")
        return # Si falla la extracción, detenemos el proceso

    if not datos_extraidos:
        logging.info("No hay datos para migrar.")
        return

    # PASO 2: Carga (Load) a PostgreSQL usando Transacciones y Parametrización
    logging.info("Iniciando carga hacia PostgreSQL...")
    try:
        with motor_pg.connect() as conn_pg:
            # Iniciamos la transacción explícitamente
            transaccion = conn_pg.begin()
            
            try:
                # Query parametrizada. Los nombres de los parámetros (:id_candidato, etc.) 
                # deben coincidir con las llaves de los diccionarios que extrajimos.
                query_insert = text("""
                    INSERT INTO candidatos_ape (id_candidato, nombre, profesion, estado) 
                    VALUES (:id_candidato, :nombre, :profesion, :estado)
                """)
                
                # Ejecutamos la inserción. En SQLAlchemy 2.0 podemos pasar la lista completa
                # de diccionarios y él optimiza la inserción (executemany por debajo)
                conn_pg.execute(query_insert, datos_extraidos)
                
                # Si todo sale bien, confirmamos los cambios en la base de datos
                transaccion.commit()
                logging.info("¡Migración completada con éxito! Todos los datos fueron guardados.")
                
            except Exception as e_carga:
                # Si ocurre un error en la inserción (ej. llave duplicada), revertimos TODO
                transaccion.rollback()
                logging.error(f"Error durante la inserción. Se realizó ROLLBACK. Detalle: {e_carga}")
                
    except Exception as e:
        logging.error(f"Error en la conexión a PostgreSQL durante la carga: {e}")

if __name__ == "__main__":
    migrar_datos()