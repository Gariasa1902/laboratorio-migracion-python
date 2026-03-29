# Importamos las librerías necesarias
import pandas as pd # pandas  para manejo de datos
from pathlib import Path # pathlib  para manejar rutas de archivos sin importar el sistema operativo
import logging # Logging básico  para registrar eventos en la terminal
from typing import Iterator # Tipado básico  para definir qué devuelve nuestra función

# Configuración del logging básico  para ver mensajes claros en consola
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Definimos nuestra función (Funciones y modularidad )
# El "-> None" indica que la función no retorna ningún valor (tipado básico )
def procesar_archivo_por_lotes(ruta_archivo: Path, tamaño_lote: int = 1000) -> None:
    """
    Lee un archivo CSV grande procesándolo en lotes pequeños para no saturar la memoria RAM.
    """
    logging.info(f"Iniciando la lectura del archivo: {ruta_archivo}")

    try:
        # En lugar de cargar todo el archivo, pandas.read_csv con 'chunksize'
        # crea un Iterador/Generator. Solo carga en memoria el 'tamaño_lote' definido.
        iterador_lotes: Iterator[pd.DataFrame] = pd.read_csv(ruta_archivo, chunksize=tamaño_lote)
        
        total_filas = 0
        
        # Iteramos sobre cada lote (chunk)
        for numero_lote, lote in enumerate(iterador_lotes, start=1):
            # 'lote' es un DataFrame de pandas que contiene solo 1000 filas (o el tamaño_lote)
            cantidad_filas = len(lote)
            total_filas += cantidad_filas
            
            # Aquí es donde haríamos la transformación de datos en el futuro.
            # Por ahora, solo registramos que estamos procesando esta porción.
            logging.info(f"Procesando lote {numero_lote}: {cantidad_filas} filas en memoria.")
            
        logging.info(f"Procesamiento exitoso. Total de filas leídas: {total_filas}")

    except FileNotFoundError:
        logging.error(f"Error: El archivo no se encontró en la ruta {ruta_archivo}")
    except Exception as e:
        logging.error(f"Ocurrió un error inesperado: {e}")

# Este bloque es el equivalente a "func main()" en Golang. 
# Indica el punto de entrada principal del script.
if __name__ == "__main__":
    # Usamos pathlib para apuntar a un archivo falso llamado 'datos_prueba.csv'
    ruta_datos = Path("datos_prueba.csv")
    
    # Llamamos a nuestra función, indicando que lea de a 500 filas por vez
    procesar_archivo_por_lotes(ruta_datos, tamaño_lote=500)