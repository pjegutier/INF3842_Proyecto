import altair as alt
import streamlit as st
from vega_datasets import data

df_1 = data.cars()
scatter  = alt.Chart(df_1).mark_point().encode(x='Horsepower', y='Miles_per_Gallon')

df_2 = data.iris()
area = alt.Chart(df_2).mark_area(color="maroon").encode(x='sepalLength', y='petalLength')

obj = alt.vconcat(scatter, area) #Vertical Concatenation

st.altair_chart(obj)
