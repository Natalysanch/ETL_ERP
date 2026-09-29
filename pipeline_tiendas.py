import os
import pandas as pd
import sqlite3
from dotenv import load_dotenv

load_dotenv()

RUTA_ARCHIVOS = os.getenv("RUTA_ARCHIVOS", "csvs")
RUTA_DB = os.getenv("RUTA_DB", "instance")

# Leer el archivo de tiendas nuevas
ruta_csv = os.path.join(RUTA_ARCHIVOS, "Tiendas_nuevas.csv")
datos_tiendas = pd.read_csv(ruta_csv)

# Conectar con la base de datos
conn = sqlite3.connect(
    os.path.join(RUTA_DB, "datacaos_estrella.db")
)

# Actualizar la dimensión Tienda
for _, tienda in datos_tiendas.iterrows():
    conn.execute("""
        INSERT OR REPLACE INTO DimTienda
        (TiendaID, NombreTienda, Ciudad, Region, FechaApertura)
        VALUES (?, ?, ?, ?, ?)
    """, (
        tienda["TiendaID"],
        tienda["NombreTienda"],
        tienda["Ciudad"],
        tienda["Region"],
        tienda["FechaApertura"]
    ))

conn.commit()
conn.close()

print(f"Se actualizaron {len(datos_tiendas)} tiendas.")