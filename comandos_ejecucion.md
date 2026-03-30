# Comandos de Ejecución - Migración Python

## Activar el entorno virtual (SIEMPRE hacer esto al abrir VS Code)
source venv/bin/activate

## Cambiar entre etapas (Ramas de Git)
Para trabajar o revisar una etapa específica:
- Ir a Etapa 1: `git checkout etapa1`
- Ir a Etapa 2: `git checkout etapa2`
- Ir a Etapa 3: `git checkout etapa3`
- Volver a la rama principal: `git checkout main`

## Ejecutar los scripts (Los crearemos en los siguientes pasos)
- Etapa 1: `python etapa1/main.py`
- Etapa 2: `python etapa2/migracion_basica.py`
- Etapa 3: `python etapa3/etl_modular.py`

## Levantar Bases de Datos (Docker)
Si reinicias el computador, asegúrate de levantar las bases de datos antes de correr el código:
`docker compose up -d`

Para detenerlas cuando termines de trabajar:
`docker compose down`

## Credenciales Locales
**PostgreSQL (Destino):**
- Host: localhost | Puerto: 5432
- DB: db_destino | Usuario: usuario_ape | Pass: password123

**Oracle (Origen):**
- Host: localhost | Puerto: 1521
- Service: XEPDB1 | Usuario: system | Pass: password123