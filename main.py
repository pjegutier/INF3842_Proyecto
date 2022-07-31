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
    st.title("🚴🏾 Rutas en Bici - Machali")

with row1_2:
    st.write(
        """
    ##
    Hola biker de Machalí, la mejor ciudad de Chile, escoge 2 rutas de tu interés para disfrutar. Podrás comparar su ubicación y altura para evaluar
    la dificultad técnica y encontrar tu próximo desafío. Atrévete te te!    
    """
    )
   
    
    # lista de rutas
    options = st.multiselect(
        'Elige hasta 2 rutas para compararlas',
        df['ns1:Name'].unique(), 
        df['ns1:Name'].unique()[:2])
    
    if len(options) > 2:
        st.write('Ha elegido más de 2 rutas, elija nuevamente, elimine selecciones')
    

row2_1, row2_2, row2_3 = st.columns((1, 1, 1))

zoom = 12 

if len(options) == 1:
    lat = np.mean(df.loc[df['ns1:Name'] == options[0]]['ns1:LatitudeDegrees4'])
    lon = np.mean(df.loc[df['ns1:Name'] == options[0]]['ns1:LongitudeDegrees5'])    
elif len(options) == 2:
    lat = (np.mean(df.loc[df['ns1:Name'] == options[0]]['ns1:LatitudeDegrees4']) + np.mean(df.loc[df['ns1:Name'] == options[1]]['ns1:LatitudeDegrees4']))/2
    lon = (np.mean(df.loc[df['ns1:Name'] == options[0]]['ns1:LongitudeDegrees5']) + np.mean(df.loc[df['ns1:Name'] == options[1]]['ns1:LongitudeDegrees5']))/2
    
else:
    lat = -34.18082 #machali
    lon = -70.64933 #machali
    
# with row2_1:
#     st.write(
#         pdk.Deck(
#             map_style="mapbox://styles/mapbox/satellite-v9",
#             initial_view_state={
#                 "latitude": lat,
#                 "longitude": lon,
#                 "zoom": zoom,
#                 "pitch": 50,}
#         )
#     )        

with row2_1:
    viewstate = pdk.ViewState(
        longitude = -70.64933,
        latitude = -34.18082,
        zoom = zoom,
        pitch = 50)
    
    df2 = df.rename(columns = {'ns1:LongitudeDegrees5':'lng', 'ns1:LatitudeDegrees4':'lat'}, inplace = True)
    
#     layer = pdk.Layer(
#         'HexagonLayer',
#         df2,
#         get_position=['lon', 'lat'],
#         auto_highlight=True,
#         elevation_scale=50,
#         pickable=True,
#         elevation_range=[0, 3000],
#         extruded=True,
#         coverage=1)
    
    layer = pdk.Layer(
        'ScatterplotLayer',
    df2,
    get_position=['lng', 'lat'],
    auto_highlight=True,
    get_radius=1000,
    get_fill_color='[180, 0, 200, 140]',
    pickable=True)
    
#     r = pdk.Deck(map_style="mapbox://styles/mapbox/satellite-v9", initial_view = viewstate)
#     r = pdk.Deck(layers=[layer], initial_view_state=view_state)
#     st.write(r)
    
    st.write(df2.head())


# primera ruta
with row2_2:
    try:
        line = alt.Chart(df.loc[df['ns1:Name'] == options[0]]).mark_circle(size=30).encode(
            x = alt.X('ns1:LatitudeDegrees4:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Latitud')),
            y = alt.Y('ns1:LongitudeDegrees5:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Longitud'))
        ).properties(width=400, height=500)

        st.altair_chart(line)
    except:
        None
    
# segunda ruta
with row2_3:
    try:
        line = alt.Chart(df.loc[df['ns1:Name'] == options[1]]).mark_circle(size=30).encode(
            x = alt.X('ns1:LatitudeDegrees4:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Latitud')),
            y = alt.Y('ns1:LongitudeDegrees5:Q',scale=alt.Scale(zero=False),axis=alt.Axis(title='Longitud')),
            color = alt.value("orange")
        ).properties(width=400, height=500)
    
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
    x=alt.X("dist_total:Q", title ='Distancia Recorrido [m]'),
    y=alt.Y("a_r:Q", stack=None, title = 'Altura Relativa [m]'),
    color= alt.Color("ns1:Name:N", title = 'Rutas'),
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
