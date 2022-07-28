import altair as alt
import pandas as pd
import numpy as np
import streamlit as st
import subprocess
import sys
import pydeck as pdk

# # funcion
# def load_data():
#     data = pd.read_csv(
#         "uber-raw-data-sep14.csv.gz",
#         nrows=100000,  # approx. 10% of data
#         names=[
#             "date/time",
#             "lat",
#             "lon",
#         ],  # specify names directly since they don't change
#         skiprows=1,  # don't read header since names specified directly
#         usecols=[0, 1, 2],  # doesn't load last column, constant value "B02512"
#         parse_dates=[
#             "date/time"
#         ],  # set as datetime instead of converting after the fact
#     )

#     return data


# cargamos base de datos
san_juan = pd.read_csv('san-juan-xl.csv',sep=';',decimal=',')
buitrera = pd.read_csv('buitrera-lastorres.csv',sep=';',decimal=',')
endubaik = pd.read_csv('endubaik-leo-larga.csv',sep=';',decimal=',')
guindal = pd.read_csv('guindal-sausal-los-mineros.csv',sep=';',decimal=',')
lastorres = pd.read_csv('lastorres-pinoskytrail-xl.csv',sep=';',decimal=',')
pabellones = pd.read_csv('pabellones.csv',sep=';',decimal=',')

st.set_page_config(layout="wide", page_icon="🚲", page_title="Rutas en Bici")



st.write('')
st.write('')

# Lay Out Superior
row1_1, row1_2 = st.columns((1, 2))

with row1_1:
    st.title("🚴🏾 Rutas en Bici")
    st.write(
        """
    ##
    Profesora: Tamara Cucumides\n
    Alumnos:   Luis Campos, Pablo Gutierrez 
    
    """
    )


with row1_2:
    st.write(
        """
    ##
    Se escoge un dataset de página wikiloc (https://es.wikiloc.com/) debido a que buscamos un tema de visualización que nos motiva.
    El dataset tiene atributos como altitud, longitud, latitud, velocidad, distancia, variables que permiten analizar una ruta desde multiples formas de visualización.
    """
    )
    # lista de rutas
    options = st.multiselect(
     'What are your favorite colors',
     ['san_juan', 'buitrera', 'endubaik', 'guindal', 'lastorres', 'pabellones'], 
        ['san_juan'], on_change = seleccion())
    
    def seleccion():
        if len(options) >= 2:
            options.disabled = True
        else:
            options.disabled = False            
            
#     button = st.button("Print Locations",disabled=False)

#     if button :
#         if len(options) <= 2:
#         st.write(options)
#     else:
#         st.warning("You have to select only 2 locations")

        #     rutas = source.symbol.unique()
#     lista_rutas = st.multiselect("Choose stocks to visualize", all_symbols, all_symbols[:3])

    
row2_1, row2_2, row2_3 = st.columns((1, 1, 1))

zoom = 12    
lat = np.average(san_juan['ns1:LatitudeDegrees4'])
lon = np.average(san_juan['ns1:LongitudeDegrees5'])

    
with row2_1:
    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/satellite-v9",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 50,}
        )
    )

# with row2_1:
#     st.write(
#          pdk.Deck(
#              map_style="mapbox://styles/mapbox/satellite-v9",
#              initial_view_state={
#                  "latitude": lat,
#                  "longitude": lon,
#                  "zoom": zoom,
#                  "pitch": 50,
#               },
#               layers=[
#                   pdk.Layer(
#                       "HexagonLayer",
#                       data=bici,
#                       get_position=['ns1:LongitudeDegrees5', 'ns1:LatitudeDegrees4'],
#                       auto_highlight=True,
#                       elevation_scale=50,
#                       pickable=True,
#                       elevation_range=[0, 3000],
#                       extruded=True,
#                       coverage=1),
#               ],
#          )
#     )

# primera ruta
with row2_2:
    try:
        line = alt.Chart(locals()[options[0]]).mark_circle(size=60).encode(
            x = alt.X('ns1:LatitudeDegrees4:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Latitud')),
            y = alt.Y('ns1:LongitudeDegrees5:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Longitud'))
        ).properties(width=500, height=500)

        st.altair_chart(line)
    except:
        None
    
# segunda ruta
with row2_3:
    try:
        line = alt.Chart(locals()[options[1]]).mark_circle(size=60).encode(
            x = alt.X('ns1:LatitudeDegrees4:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Latitud')),
            y = alt.Y('ns1:LongitudeDegrees5:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Longitud'))
        ).properties(width=500, height=500)
    
        st.altair_chart(line)
    except:
        None

# # segunda ruta
# with row2_4:
#     line = alt.Chart(endubaik).mark_circle(size=60).encode(
#         x = alt.X('ns1:LatitudeDegrees4:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Latitud')),
#         y = alt.Y('ns1:LongitudeDegrees5:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Longitud'))
#     ).properties(width=500, height=500)
    
#     st.altair_chart(line)

# # segunda ruta
# with row2_5:
#     line = alt.Chart(guindal).mark_circle(size=60).encode(
#         x = alt.X('ns1:LatitudeDegrees4:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Latitud')),
#         y = alt.Y('ns1:LongitudeDegrees5:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Longitud'))
#     ).properties(width=500, height=500)
    
#     st.altair_chart(line)

# with row2_6:
#     line = alt.Chart(lastorres).mark_circle(size=60).encode(
#         x = alt.X('ns1:LatitudeDegrees4:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Latitud')),
#         y = alt.Y('ns1:LongitudeDegrees5:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Longitud'))
#     ).properties(width=500, height=500)
    
#     st.altair_chart(line)

# with row2_7:
#     line = alt.Chart(pabellones).mark_circle(size=60).encode(
#         x = alt.X('ns1:LatitudeDegrees4:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Latitud')),
#         y = alt.Y('ns1:LongitudeDegrees5:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Longitud'))
#     ).properties(width=500, height=500)
    
#     st.altair_chart(line)
   
st.write(san_juan.head())
