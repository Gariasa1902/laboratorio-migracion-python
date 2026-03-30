# Proyecto de Migración APE - Python

# Laboratorio de Migración de Datos (Oracle a PostgreSQL) - Python

Este proyecto es un laboratorio de entrenamiento para el desarrollo de un sistema de migración de datos utilizando Python. Implementa un pipeline ETL modular, procesamiento por lotes (Chunking), manejo de transacciones y validación de integridad.

## Requisitos Previos
- Python 3.14 (o superior)
- Docker y Docker Desktop
- DBeaver (Opcional, para visualización)

## 1. Configuración Inicial (Solo se hace una vez)

### Levantar la Infraestructura (Bases de Datos)
```bash
docker compose up -d

### Activar el Entorno Virtual
source venv/bin/activate

### Ejecución por Etapas
## Lee archivos pesados sin saturar la memoria RAM.
git checkout etapa1
python generar_datos.py           # Genera un CSV de 50,000 registros
python etapa1/procesar_archivos.py # Procesa el archivo en lotes

### Conexión a DB y Migración Básica
## Conecta a Oracle y PostgreSQL usando SQLAlchemy y realiza una extracción y carga segura con transacciones.
git checkout etapa2
python etapa2/conexion_db.py         # Prueba de conexión a los motores
python etapa2/preparar_entorno_db.py # Crea tablas e inserta datos de prueba
python etapa2/migracion_basica.py    # Ejecuta la migración con transacciones

### ETL Modular, Resiliencia y Validación
## Implementa un ETL que puede reanudarse ante caídas (Checkpoints) y valida la integridad de los datos mediante Hash/Checksum.
git checkout etapa3
python etapa3/generar_volumen_oracle.py # Genera 10,000 registros en Oracle
python etapa3/etl_modular.py            # Ejecuta el ETL (puedes detenerlo con Ctrl+C y reanudarlo)
python etapa3/validacion_datos.py       # Valida conteos cruzados y Checksum MD5

### Apagar el entorno
## Al finalizar la jornada de trabajo, detén los contenedores para liberar recursos:
docker compose down

