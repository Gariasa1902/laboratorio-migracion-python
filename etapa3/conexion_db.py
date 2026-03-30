import logging
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

# Configuramos el logging para ver qué sucede en la terminal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def obtener_conexion_postgres() -> Engine:
    """
    Crea y retorna el motor de conexión para PostgreSQL usando SQLAlchemy.
    """
    # URL de conexión: dialecto+driver://usuario:password@host:puerto/base_de_datos
    url_postgres = "postgresql+psycopg2://usuario_ape:password123@localhost:5432/db_destino"
    
    try:
        # create_engine crea la "fábrica" de conexiones
        motor = create_engine(url_postgres)
        logging.info("Motor de PostgreSQL creado correctamente.")
        return motor
    except Exception as e:
        logging.error(f"Error al crear la conexión a PostgreSQL: {e}")
        raise e

def obtener_conexion_oracle() -> Engine:
    """
    Crea y retorna el motor de conexión para Oracle usando SQLAlchemy y oracledb.
    """
    # URL de conexión: dialecto+driver://usuario:password@host:puerto/?service_name=servicio
    url_oracle = "oracle+oracledb://system:password123@localhost:1521/?service_name=XEPDB1"
    
    try:
        motor = create_engine(url_oracle)
        logging.info("Motor de Oracle creado correctamente.")
        return motor
    except Exception as e:
        logging.error(f"Error al crear la conexión a Oracle: {e}")
        raise e

# Bloque de prueba (Main)
if __name__ == "__main__":
    logging.info("Probando conexiones a las bases de datos...")
    
    motor_pg = obtener_conexion_postgres()
    motor_or = obtener_conexion_oracle()
    
    # Probamos PostgreSQL
    try:
        # Usamos un bloque 'with' (context manager). Es similar al 'defer' en Golang,
        # asegura que la conexión se cierre automáticamente al terminar el bloque.
        with motor_pg.connect() as conn_pg:
            resultado = conn_pg.execute(text("SELECT version();")).scalar()
            logging.info(f"Conexión exitosa a PG. Versión: {resultado[:25]}...")
    except Exception as e:
        logging.error(f"Falló la prueba de PostgreSQL: {e}")

    # Probamos Oracle
    try:
        with motor_or.connect() as conn_or:
            resultado = conn_or.execute(text("SELECT * FROM v$version")).first()
            logging.info(f"Conexión exitosa a Oracle. Versión: {resultado[0][:30]}...")
    except Exception as e:
        logging.error(f"Falló la prueba de Oracle: {e}")