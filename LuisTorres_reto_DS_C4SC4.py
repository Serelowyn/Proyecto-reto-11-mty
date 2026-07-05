# -------------- Importaciones

import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt

# -------------- Fin de las importaciones Importaciones

""" se carga el csv de datos de empleados del reto"""
df = pd.read_csv(r"C:\\Users\\sasor\\Desktop\\Tec de mty\\4. Diseño de interfaces visuales ne python\\3. Aplicacion web de ciencia de datos\\reto\\Employee_data.csv")

"""empiezo por revisar la integridad de las columnas para verificar si posteriormente necesito hacer una limpieza del df"""

print(df.head())
# se detecta error en gender columna
# se detecta error en manager id donde el tipo es erroneo, y hay espacioes en NaN

print(df.shape)
print(df.dtypes)
print(df.info)
print(df.columns)

"""en el caseo de la columna: "gender" se detectaron espacios de mas; se procede a primero pasar a integer la columna del id del manager pero rellenando con un id nuevo que simule la falta de informacion, o sea 0 en este caso. en nonbre de empleado se quitan espacions adicionales y comas."""
df["manager_id"] = df["manager_id"].fillna(0).astype(int)
df["gender"] = df["gender"].str.strip()

"""en este caso algunos nombres tienen doble espacio al final, o mas. se aplica el mismo filtro mas veces hasta que quede limpio"""
df["name_employee"] = (df["name_employee"].str.replace(",", "", regex=False).str.replace("  ", " ", regex=False).str.replace("  ", " ", regex=False).str.strip())

