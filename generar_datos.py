import pandas as pd
import random

print("Generando archivo de prueba con 10.000.000 registros...")

# Creamos una lista de diccionarios con datos simulados
datos = []
for i in range(1, 10000001):
    datos.append({
        'id_usuario': i,
        'nombre': f'Usuario_APE_{i}',
        'estado': random.choice(['Activo', 'Inactivo', 'Pendiente'])
    })

# Usamos pandas para convertir la lista en un DataFrame y guardarlo como CSV
df = pd.DataFrame(datos)
df.to_csv('datos_prueba.csv', index=False)

print("Archivo 'datos_prueba.csv' generado con éxito.")