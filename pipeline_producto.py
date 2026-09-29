import os
import pandas as pd
import sqlite3
from dotenv import load_dotenv

load_dotenv()

RUTA_ARCHIVOS = os.getenv("RUTA_ARCHIVOS", "csvs")
RUTA_DB = os.getenv("RUTA_DB", "instance")

# Leer el archivo de productos nuevos
ruta_csv = os.path.join(RUTA_ARCHIVOS, "Productos_nuevos.csv")
datos_productos = pd.read_csv(ruta_csv)

# Conectar con la base de datos
conn = sqlite3.connect(
    os.path.join(RUTA_DB, "datacaos_estrella.db")
)

# Actualizar la dimensión Producto
for _, producto in datos_productos.iterrows():

    conn.execute("""
        INSERT OR REPLACE INTO DimProducto
        (ProductoID, NombreProducto, MarcaProducto,
         NombreCategoria, NombreProveedor, PaisProveedor, PrecioListado)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        producto["ProductoID"],
        producto["NombreProducto"],
        producto["MarcaProducto"],
        producto["NombreCategoria"],
        producto["NombreProveedor"],
        producto["PaisProveedor"],
        producto["PrecioListado"]
    ))

conn.commit()
conn.close()

print(f"Se actualizaron {len(datos_productos)} productos.")