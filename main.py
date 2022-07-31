import altair as alt
import pandas as pd
import numpy as np
import streamlit as st
import subprocess
import sys
import pydeck as pdk



# cargamos base de datos
san_juan = pd.read_csv('san-juan-xl.csv',sep=',',decimal='.')
buitrera = pd.read_csv('buitrera-lastorres.csv',sep=',',decimal='.')
endubaik = pd.read_csv('endubaik-leo-larga.csv',sep=',',decimal='.')
guindal = pd.read_csv('guindal-sausal-los-mineros.csv',sep=',',decimal='.')
lastorres = pd.read_csv('lastorres-pinoskytrail-xl.csv',sep=',',decimal='.')
pabellones = pd.read_csv('pabellones.csv',sep=',',decimal='.')


# Calculamos distancia acumulada
san_juan['dist_total'] = san_juan['d_r'].cumsum()
buitrera['dist_total'] = buitrera['d_r'].cumsum()
endubaik['dist_total'] = endubaik['d_r'].cumsum()
guindal['dist_total'] = guindal['d_r'].cumsum()
lastorres['dist_total'] = lastorres['d_r'].cumsum()
pabellones['dist_total'] = pabellones['d_r'].cumsum()

df = pd.concat([san_juan, buitrera, endubaik, guindal, lastorres, pabellones], ignore_index = True)

st.set_page_config(layout="wide", page_icon="🚲", page_title="Rutas en Bici")

st.write('')
st.write('')

# Lay Out Superior
row1_1, row1_2 = st.columns((1, 2))

with row1_1:
    st.title("🚴🏾 Rutas en Bici")

with row1_2:
    st.write(
        """
    ##
    Hola biker de Machalí, escoge 2 rutas de tu interés para ver su ubicación, altura comparativa 
    
    
    .
    """
    )
   
    
    # lista de rutas
    options = st.multiselect(
        'Elige hasta 2 rutas para compararlas',
        df['ns1:Name'].unique(), 
        df['ns1:Name'].unique()[:2])
    
    if len(options) > 2:
        st.write('Ha elegido más de 2 rutas, elija nuevamente, elimine selecciones')
    
            
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
lat = np.average(np.average(df.loc[df['ns1:LatitudeDegrees4'] == options[0]]),np.average(df.loc[df['ns1:LatitudeDegrees4'] == options[1]]))
lon = np.average(np.average(df.loc[df['ns1:LongitudeDegrees5'] == options[0]]),np.average(df.loc[df['ns1:LongitudeDegrees5'] == options[1]])) 
    
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
        line = alt.Chart(df.loc[df['ns1:Name'] == options[0]]).mark_circle(size=60).encode(
            x = alt.X('ns1:LatitudeDegrees4:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Latitud')),
            y = alt.Y('ns1:LongitudeDegrees5:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Longitud'))
        ).properties(width=500, height=500)

        st.altair_chart(line)
    except:
        None
    
# segunda ruta
with row2_3:
    try:
        line = alt.Chart(df.loc[df['ns1:Name'] == options[1]]).mark_circle(size=60).encode(
            x = alt.X('ns1:LatitudeDegrees4:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Latitud')),
            y = alt.Y('ns1:LongitudeDegrees5:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Longitud'))
        ).properties(width=500, height=500)
    
        st.altair_chart(line)
    except:
        None

st.write("")
st.write("")

if len(options) == 0:
    datos_sel = pd.DataFrame()
elif len(options) == 1:
    datos_sel = df.loc[df['ns1:Name'] == options[0]]
else: 
    datos_sel = df.loc[(df['ns1:Name'] == options[0]) | (df['ns1:Name'] == options[1])]
    

selection = alt.selection_multi(fields=['ns1:Name'], bind='legend')

chart = alt.Chart(datos_sel).mark_area().encode(
    x="dist_total:Q",
    y=alt.Y("a_r:Q", stack=None),
    color= "ns1:Name:N",
    opacity=alt.condition(selection, alt.value(1.0), alt.value(0.3)) 
).properties(width=1300, height=200).add_selection(selection)

# mostrar gráfico de altair
st.altair_chart(chart)

st.write(   
    """
    ##
    Profesora: Tamara Cucumides\n
    Alumnos:   Luis Campos, Pablo Gutierrez 
    
    """
)
