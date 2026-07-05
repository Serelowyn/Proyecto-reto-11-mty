# -------------- Importaciones

import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt
from PIL import Image
import plotly.express as px

# -------------- Fin de las importaciones Importaciones

# se carga el csv de datos de empleados del reto
df = pd.read_csv(r"C:\\Users\\sasor\\Desktop\\Tec de mty\\4. Diseño de interfaces visuales ne python\\3. Aplicacion web de ciencia de datos\\reto\\Employee_data.csv")

# empiezo por revisar la integridad de las columnas para verificar si posteriormente necesito hacer una limpieza del df

print(df.head())
# se detecta error en gender columna
# se detecta error en manager id donde el tipo es erroneo, y hay espacioes en NaN

print(df.shape)
print(df.dtypes)
print(df.info)
print(df.columns)

# en el caseo de la columna: "gender" se detectaron espacios de mas; se procede a primero pasar a integer la columna del id del manager pero rellenando con un id nuevo que simule la falta de informacion, o sea 0 en este caso. en nonbre de empleado se quitan espacions adicionales y comas.
df["manager_id"] = df["manager_id"].fillna(0).astype(int)
df["gender"] = df["gender"].str.strip()

# en este caso algunos nombres tienen doble espacio al final, o mas. se aplica el mismo filtro mas veces hasta que quede limpio
df["name_employee"] = (df["name_employee"].str.replace(",", "", regex=False).str.replace("  ", " ", regex=False).str.replace("  ", " ", regex=False).str.strip())

# titulo y descripcion de la app
st.title("analisis de desempeno de colaboradores")
st.write("aplicacion web para el area de marketing de socialize your knowledge. aqui se revisa el desempeno de los colaboradores junto con sus horas trabajadas, salario, edad y estado civil.")

# logo de la empresa 
logo = Image.open("logo_d_reto.png")
st.image(logo, width=220)

# barra de filtros en la izquierda
st.sidebar.header("filtros")

# filtro de genero de empleado
selected_gender = st.sidebar.radio("selecciona el genero", df["gender"].unique())

# control para seleccionar el rango del puntaje de desempeno
min_score = int(df["satisfaction_level"].min())
max_score = int(df["satisfaction_level"].max())
score_range = st.sidebar.slider("rango del puntaje de desempeno",min_score,max_score,(min_score, max_score))

# control para seleccionar el estado civil del empleado
selected_marital = st.sidebar.selectbox("selecciona el estado civil", df["marital_status"].unique())

# se aplican los filtros de los controles a un subconjunto que se muestra en tabla
filtered = df[(df["gender"] == selected_gender) & (df["performance_score"] >= score_range[0]) & (df["performance_score"] <= score_range[1]) & (df["marital_status"] == selected_marital)]

st.subheader("empleados que cumplen con los filtros")
st.write("registros encontrados:", filtered.shape[0])
st.dataframe(filtered[["name_employee", "gender", "marital_status", "performance_score", "salary", "age", "average_work_hours"]])

# grafica de la distribucion de los puntajes de desempeno en general
st.subheader("distribucion de los puntajes de desempeno")
fig1 = px.histogram(df, x="performance_score", nbins=5)
st.plotly_chart(fig1, use_container_width=True)

# grafico del promedio de horas trabajadas por genero
st.subheader("promedio de horas trabajadas por genero")
horas_genero = df.groupby("gender")["average_work_hours"].mean().reset_index()
fig2 = px.bar(horas_genero, x="gender", y="average_work_hours", color="gender")
st.plotly_chart(fig2, use_container_width=True)

# grafico de la edad de los empleados con respecto al salario
st.subheader("edad vs salario")
fig3 = px.scatter(df, x="age", y="salary", color="gender")
st.plotly_chart(fig3, use_container_width=True)

# grafico del promedio de horas trabajadas - el puntaje de desempeno
st.subheader("promedio de horas trabajadas vs puntaje de desempeno")
horas_score = df.groupby("performance_score")["average_work_hours"].mean().reset_index()
fig4 = px.bar(horas_score, x="performance_score", y="average_work_hours")
st.plotly_chart(fig4, use_container_width=True)

# conclusiones del analisis
st.subheader("Conclusion")
st.write("la mayoria de los colaboradores se concentra en los puntajes de desempeno mas aceptables, aunque hay mas trabajadores en los extremos buenos de calificacion 4 y 5 que en los extremos de 1 y 2, en general el area mantiene un buen nivel... el promedio de horas trabajadas es parecido entre generos, no hay una diferencia significante, la pequeña variacion puede ser debido a cualquier situacion personal extraordinaria; en la edad y salario se nota que el salario no depende solo de la edad, hay puestos que pagan mas sin importar la cantidad de tiempo que tenga la persona. y al comparar las horas trabajadas contra el puntaje de desempeno no creo que sea posible concluir que hay una relacion fuerte entre el tiempo de trabajo y el puntaje por lo que trabajar mas horas no significa un mejor puntaje")
