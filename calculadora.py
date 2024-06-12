# Librerias a utilizar
from fastapi import FastAPI, HTTPException
from typing import List, Dict
import pandas as pd
from datetime import datetime
from unidecode import unidecode
from pydantic import BaseModel
import uvicorn
import os
import numpy as np

# Obtiene el directorio actual del archivo
current_directory = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
# Construye la ruta al archivo de datos en la carpeta 'dataset_limpios'
file_path_productos = os.path.join(current_directory, "productos.xlsx")
# Carga los archivos para realizar consultas
productos = pd.read_excel(file_path_productos)

# Pone nombre, descripción y versión a la API
app = FastAPI(title='Sistema de gestión comercio virtual multiplataforma',
              description='Herramienta para cálculo de ganacias y gestión de inventario',
              version='1.0')


# End point de prueba
@app.get("/")
def read_root():
    return {"Bienvenido al sistema de gestión"}

@app.get("/ganancias/{id_producto}")
def ganancias(id_producto: int, plataforma: str, costo_envio: int):
    if id_producto in productos['sku']:
        df_sku = productos[productos['sku'] == id_producto]
        if plataforma == 'precio de venta p1':        
            ganancia = df_sku['precio de venta p1'] - df_sku['costo producto'] - costo_envio
            cantidad = df_sku['cantidad'] - 1
            mensaje = f"La ganancia es de ${ganancia.values[0]}. Quedan {cantidad.values[0]} unidades."
        elif plataforma == 'precio de venta p2':
            comision = df_sku['precio de venta p2']* 0.22
            ganancia = df_sku['precio de venta p2'] - df_sku['costo producto'] - costo_envio - comision
            cantidad = df_sku['cantidad'] - 1
            mensaje = f"La ganancia es de ${ganancia.values[0]}. Quedan {cantidad.values[0]} unidades."
    else: 
        mensaje = 'No existe un producto con este SKU.'

    return mensaje