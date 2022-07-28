import altair as alt
import pandas as pd
import streamlit as st
import subprocess
import sys
import pydeck as pdk

# funcion
def load_data():
    data = pd.read_csv(
        "uber-raw-data-sep14.csv.gz",
        nrows=100000,  # approx. 10% of data
        names=[
            "date/time",
            "lat",
            "lon",
        ],  # specify names directly since they don't change
        skiprows=1,  # don't read header since names specified directly
        usecols=[0, 1, 2],  # doesn't load last column, constant value "B02512"
        parse_dates=[
            "date/time"
        ],  # set as datetime instead of converting after the fact
    )

    return data


# cargamos base de datos
bici = pd.read_csv('san-juan-xl.csv',sep=';',decimal=',')

st.set_page_config(layout="centered", page_icon="🚲", page_title="Rutas en Bici")

# Rutas en Bici

st.title("🚴🏾 Rutas en Bici")

# lista de rutas
# rutas = source.symbol.unique()
# lista_rutas = st.multiselect("Choose stocks to visualize", all_symbols, all_symbols[:3]

st.write('Profesora: Tamara Cucumides')
st.write('Alumnos: Luis Campos, Pablo Gutierrez')

subprocess.check_call([sys.executable, "-m", "pip", "install", 'lxml'])

line = alt.Chart(bici).mark_circle(size=60).encode(
    x = alt.X('ns1:LatitudeDegrees4:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Latitud')),
    y = alt.Y('ns1:LongitudeDegrees5:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Latitud'))
).properties(width=500, height=500).interactive()

st.write('Se escoge un dataset de página wikiloc (https://es.wikiloc.com/) debido a que buscamos un tema de visualización que nos motiva.'
          'El dataset tiene atributos como altitud, longitud, latitud, velocidad, distancia, variables que permiten analizar una ruta desde'
          'multiples formas de visualización')

st.altair_chart(line)
st.write(bici.head())

