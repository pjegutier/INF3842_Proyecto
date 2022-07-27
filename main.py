import altair as alt
import pandas as pd
import streamlit as st
import subprocess
import sys

st.set_page_config(layout="centered", page_icon="🚲", page_title="Rutas en Bici")

# Rutas en Bici

st.title("🚲 Rutas en Bici")

st.write('Profesora: Tamara Cucumides')
st.write('Alumnos: Luis Campos, Pablo Gutierrez')

subprocess.check_call([sys.executable, "-m", "pip", "install", 'lxml'])

bici = pd.read_csv('san-juan-xl.csv',sep=';',decimal=',')

line = alt.Chart(bici).mark_circle(size=60).encode(
    x = 'ns1:LatitudeDegrees4:Q',
    y = 'ns1:LongitudeDegrees5:Q'
).properties(width=500, height=500).interactive()

st.write('Se escoge un dataset de página wikiloc (https://es.wikiloc.com/) debido a que buscamos un tema de visualización que nos motiva.'
          'El dataset tiene atributos como altitud, longitud, latitud, velocidad, distancia, variables que permiten analizar una ruta desde'
          'multiples formas de visualización')

st.altair_chart(line)
st.write(bici.head())

