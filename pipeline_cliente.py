import os
import pandas as pd
import sqlite3
from dotenv import load_dotenv

load_dotenv()

RUTA_ARCHIVOS = os.getenv("RUTA_ARCHIVOS", "csvs")
RUTA_DB = os.getenv("RUTA_DB", "instance")

# Leer el archivo de clientes nuevos
ruta_csv = os.path.join(RUTA_ARCHIVOS, "clientes_nuevos.csv")
datos_clientes = pd.read_csv(ruta_csv)

# Conectar con la base de datos
conn = sqlite3.connect(os.path.join(RUTA_DB, "datacaos_estrella.db"))

# Actualizar la dimensión Cliente
for _, cliente in datos_clientes.iterrows():
    conn.execute("""
        INSERT OR REPLACE INTO DimCliente
        (ClienteID, NombreCliente, Genero, RangoEdad, Ciudad, SegmentoCliente)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        cliente["ClienteID"],
        cliente["NombreCliente"],
        cliente["Genero"],
        cliente["RangoEdad"],
        cliente["Ciudad"],
        cliente["SegmentoCliente"]
    ))

conn.commit()
conn.close()

print(f"Se actualizaron {len(datos_clientes)} clientes.")   